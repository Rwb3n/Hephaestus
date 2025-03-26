# Proposal: BestOfNBuilder and FlowBuilderNode Integration

## Overview

This proposal outlines improvements to the integration between the `BestOfNBuilder` and `FlowBuilderNode` components in the Hephaestus system. These components are central to the system's evolutionary capability, but the current implementation has inconsistencies and missing connections. Enhancing this integration will strengthen Hephaestus' core functionality and better realize its potential as a self-improving system.

## Current State Assessment

Based on the analysis in `engine/analysis.md`, we've identified several issues:

1. **Duplicated Implementation**: Two separate implementations of `BestOfNBuilder` exist—one in `engine/best_of_n.py` (standalone class) and another in `scoring/scoring.py` (extends Node).

2. **Missing Integration**: The `scoring/scoring.py` implementation has placeholder code for variant generation rather than calling the FlowBuilderNode.

3. **Undefined Interaction**: The relationship between BestOfNBuilder and MutationEngine is not clearly defined in the code.

4. **Limited Feedback Loop**: Current implementations lack robust feedback mechanisms between scoring results and future generations.

## Implementation Objectives

The primary goal is to consolidate and enhance the relationship between these components to create a more coherent evolutionary pipeline. Specific objectives include:

1. **Consolidate BestOfNBuilder**: Create a single, consistent implementation that follows the Node pattern.

2. **Formalize Integration Points**: Define clear interfaces between BestOfNBuilder, MutationEngine, and FlowBuilderNode.

3. **Implement Feedback Mechanism**: Create a structured way for successful patterns to influence future generations.

4. **Enhance Variant Diversity**: Ensure that generated variants are meaningfully different to promote exploration.

5. **Support Parallel Generation**: Add support for concurrent variant generation to improve efficiency.

## Technical Implementation

### 1. Consolidated BestOfNBuilder

```python
# Proposed implementation in scoring/best_of_n.py
class BestOfNBuilder(Node):
    """
    Builds N variants of a concept, scores them, and selects the best.
    
    This node orchestrates:
    1. Directive mutation via MutationEngine
    2. Code generation via FlowBuilderNode
    3. Testing via TestHarness
    4. Scoring and selection of the best variant
    """
    
    def __init__(self, n: int = 3, registry: Registry = None, 
                 mutation_engine=None, flow_builder=None, test_harness=None):
        """
        Initialize the BestOfNBuilder.
        
        Args:
            n: Number of variants to build
            registry: Registry instance for scoring and recording
            mutation_engine: MutationEngine instance
            flow_builder: FlowBuilderNode instance
            test_harness: TestHarness instance
        """
        super().__init__(max_retries=1)
        self.n = n
        self.registry = registry
        
        # Initialize component instances or use provided ones
        self.mutation_engine = mutation_engine or MutationEngine()
        self.flow_builder = flow_builder or FlowBuilderNode()
        self.test_harness = test_harness or TestHarness()
        
        self.logger = logging.getLogger("BestOfNBuilder")
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Extract build task, directive, and registry."""
        build_task = shared.get("build_task", "")
        directive = shared.get("directive", {})
        registry = shared.get("registry", self.registry)
        
        return {
            "build_task": build_task,
            "directive": directive,
            "registry": registry
        }
    
    def exec(self, prep_res: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate N variants using mutation and flow builder."""
        build_task = prep_res.get("build_task", "")
        directive = prep_res.get("directive", {})
        registry = prep_res.get("registry")
        
        variants = []
        
        # Generate N variants
        for i in range(self.n):
            # 1. Create variation of the task and directive
            mutated_task, mutated_directive = self.mutation_engine.mutate(
                build_task, directive
            )
            
            # 2. Build variant using flow builder
            variant_shared = {
                "build_task": mutated_task,
                "directive": mutated_directive,
                "registry": registry,
                "variant_idx": i
            }
            
            # Run flow builder
            self.flow_builder.run(variant_shared)
            
            # 3. Test the generated code
            if "code" in variant_shared:
                test_shared = variant_shared.copy()
                self.test_harness.run(test_shared)
                
                # 4. Score the result
                score = test_shared.get("score", 0.0)
                
                variants.append({
                    "build_task": mutated_task,
                    "directive": mutated_directive,
                    "code": variant_shared.get("code", ""),
                    "test_results": test_shared.get("test_results", {}),
                    "score": score,
                    "class_name": variant_shared.get("class_name", ""),
                    "file_path": variant_shared.get("file_path", ""),
                    "variant_idx": i
                })
            else:
                self.logger.warning(f"Failed to generate code for variant {i}")
        
        self.logger.info(f"Generated {len(variants)} variants")
        return variants
    
    def post(self, shared: Dict[str, Any], prep_res: Dict[str, Any], 
             exec_res: List[Dict[str, Any]]) -> str:
        """Select best variant and update shared store."""
        if not exec_res:
            self.logger.warning("No variants were generated")
            return "fail"
        
        # Find highest scoring variant
        best_variant = max(exec_res, key=lambda v: v.get("score", 0.0))
        best_score = best_variant.get("score", 0.0)
        
        # Update shared with best variant info
        shared.update({
            "code": best_variant.get("code", ""),
            "test_results": best_variant.get("test_results", {}),
            "score": best_score,
            "class_name": best_variant.get("class_name", ""),
            "file_path": best_variant.get("file_path", ""),
            "build_task": best_variant.get("build_task", ""),
            "directive": best_variant.get("directive", {})
        })
        
        # Store all variants for analysis and feedback
        shared["variants"] = exec_res
        
        # Provide feedback
        shared["feedback"] = {
            "best_variant_idx": best_variant.get("variant_idx", 0),
            "best_score": best_score,
            "variant_count": len(exec_res),
            "score_range": [min(v.get("score", 0.0) for v in exec_res),
                           max(v.get("score", 0.0) for v in exec_res)]
        }
        
        self.logger.info(f"Selected best variant with score {best_score:.2f}")
        
        if best_score > shared.get("score_threshold", 0.7):
            return "success"
        else:
            return "fail"
```

### 2. Enhanced MutationEngine Interface

```python
class MutationEngine(Node):
    """
    Applies controlled variation to build tasks and directives.
    """
    
    def mutate(self, build_task: str, directive: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Mutate a build task and directive.
        
        Args:
            build_task: The original build task
            directive: The original directive
            
        Returns:
            Tuple of (mutated_task, mutated_directive)
        """
        # Use LLM to create variations
        # (Implementation details omitted for brevity)
        pass
```

### 3. Integration with ForgeLoop

```python
class ForgeLoop:
    """
    Orchestrates the Hephaestus build cycle.
    """
    
    def __init__(self, n_variants=3):
        # Initialize components
        self.goal_proposer = GoalProposer()
        self.best_builder = BestOfNBuilder(n=n_variants)
        self.registry = Registry()
        
    def step(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run one cycle of the Hephaestus build process.
        """
        # 1. Propose a build task
        action = self.goal_proposer.run(shared)
        
        # 2. Build variants, test, select best
        action = self.best_builder.run(shared)
        
        # 3. Register the result
        if action == "success":
            self.registry.register_build(shared)
            
        return shared.get("feedback", {})
```

## Implementation Plan

### Phase 1: Consolidation (Week 1)
1. Create a new consolidated `BestOfNBuilder` implementation
2. Update all references to use the new implementation
3. Add tests for the new implementation

### Phase 2: Integration Enhancement (Week 2)
1. Improve `MutationEngine` to create more diverse variants
2. Enhance integration with `FlowBuilderNode`
3. Create better interfaces between components
4. Add metrics tracking for variant diversity

### Phase 3: Feedback Mechanism (Week 3)
1. Implement a structured feedback system
2. Add historical pattern analysis
3. Create a feature to influence future generations based on past success

### Phase 4: Parallel Execution (Week 4)
1. Add support for concurrent variant generation
2. Implement progress tracking during generation
3. Add throttling capabilities for API rate limits

## Success Criteria

This integration will be considered successful if:

1. The code duplication is eliminated and replaced with a single, robust implementation
2. Variants show meaningful diversity that leads to higher-quality solutions
3. Feedback from previous generations demonstrably influences future builds
4. The system can generate, test, and score multiple variants efficiently
5. Test coverage for the integration is comprehensive

## Future Considerations

Following this integration, we could consider:

1. **Advanced Selection Methods**: Implement tournament selection or other evolutionary algorithms
2. **Self-adaptive Mutation**: Allow mutation parameters to evolve based on success
3. **Incremental Learning**: Build a meta-model of successful patterns over time
4. **Interactive Evolution**: Add human-in-the-loop selection for certain builds
5. **Distributed Generation**: Support variant generation across multiple machines

## Conclusion

Improving the integration between `BestOfNBuilder` and `FlowBuilderNode` is essential for realizing Hephaestus' vision as a self-improving system. This proposal outlines a clear path toward strengthening this integration while addressing current limitations. The result will be a more coherent, powerful evolutionary pipeline that can drive the system's ability to improve its own components over time. 