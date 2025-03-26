import os
import logging
import time
from typing import Dict, List, Any, Optional, Union, Tuple

from nodes.base_node import Node
from nodes.flow import Flow, BatchFlow
from registry.registry import Registry
from scoring.scoring import Scorer, BestOfNBuilder
from scoring.test_harness import TestHarness
from engine.goal_proposer import GoalProposer
from engine.mutation_engine import MutationEngine
from engine.flow_builder import FlowBuilderNode

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ForgeLoop(Flow):
    """
    ForgeLoop is the core recursive execution cycle of Hephaestus.
    
    It orchestrates the entire build process:
    1. Goal proposal
    2. Mutation
    3. Code generation
    4. Testing
    5. Scoring
    6. Registry updates
    
    This is where the system becomes self-improving.
    """
    
    def __init__(
        self, 
        registry_path: str = None,
        n_variants: int = 3,
        score_threshold: float = 0.7,
        entropy: float = 0.3,
        max_iterations: int = None,
        emergency_stop_path: str = "emergency_stop.flag"
    ):
        """
        Initialize the ForgeLoop.
        
        Args:
            registry_path: Path to the registry
            n_variants: Number of variants to generate per task
            score_threshold: Minimum score for a build to be considered successful
            entropy: Entropy level for mutations (0.0-1.0)
            max_iterations: Maximum number of iterations (None for unlimited)
            emergency_stop_path: Path to emergency stop flag file
        """
        # Initialize components
        self.registry = Registry(registry_path)
        self.goal_proposer = GoalProposer()
        self.mutation_engine = MutationEngine(entropy=entropy)
        self.test_harness = TestHarness()
        self.scorer = Scorer(registry=self.registry)
        
        # Set up the BestOfN builder
        self.best_builder = BestOfNBuilder(n=n_variants, registry=self.registry)
        
        # Create flow builders for each variant
        flow_builders = []
        for i in range(n_variants):
            builder = FlowBuilderNode()
            builder.set_params({"variant_idx": i})
            flow_builders.append(builder)
        
        # Connect the complete flow
        self.goal_proposer >> self.mutation_engine
        
        # Connect each builder to the test harness and scorer
        for builder in flow_builders:
            self.mutation_engine >> builder
            builder >> self.test_harness
            
            # Success path: Score then record in registry
            self.test_harness - "success" >> self.scorer
            
            # Failure path: Skip scoring and record failure
            self.test_harness - "fail" >> self.goal_proposer
            
        # Connect scorer back to goal proposer to close the loop
        self.scorer - "success" >> self.goal_proposer
        self.scorer - "fail" >> self.goal_proposer
        
        # Initialize the Flow with the goal proposer as the start node
        super().__init__(start=self.goal_proposer, name="ForgeLoop")
        
        # Store configuration
        self.n_variants = n_variants
        self.score_threshold = score_threshold
        self.entropy = entropy
        self.max_iterations = max_iterations
        self.emergency_stop_path = emergency_stop_path
        self.iteration = 0
        
        self.logger = logging.getLogger("ForgeLoop")
    
    def run_forge(self, shared: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run the forge loop for the specified number of iterations.
        
        Args:
            shared: Initial shared data store
            
        Returns:
            Final state of the shared data store
        """
        # Initialize shared state if not provided
        if shared is None:
            shared = {}
        
        # Add necessary configuration to shared
        shared.setdefault("registry", self.registry)
        shared.setdefault("score_threshold", self.score_threshold)
        
        self.logger.info(f"Starting forge loop with {self.n_variants} variants per task, entropy {self.entropy}")
        
        try:
            # Run until max iterations or emergency stop
            while True:
                # Check for emergency stop
                if os.path.exists(self.emergency_stop_path):
                    self.logger.warning("Emergency stop flag detected. Halting.")
                    break
                
                # Check if we've reached max iterations
                if self.max_iterations is not None and self.iteration >= self.max_iterations:
                    self.logger.info(f"Reached maximum iterations ({self.max_iterations}). Stopping.")
                    break
                
                # Increment iteration counter
                self.iteration += 1
                self.logger.info(f"Running forge iteration {self.iteration}")
                
                # Run a single iteration of the forge flow
                action = super().run(shared)
                
                # Log information about this iteration
                self.logger.info(f"Iteration {self.iteration} completed with action: {action}")
                
                # Allow for rate limiting
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received. Stopping gracefully.")
        except Exception as e:
            self.logger.error(f"Error in forge loop: {str(e)}", exc_info=True)
        
        self.logger.info(f"Forge loop completed after {self.iteration} iterations")
        return shared

class HephaestusEngine:
    """
    Main entry point for the Hephaestus system.
    
    Handles initialization and configuration of the forge loop.
    """
    
    def __init__(self, n_variants=3, registry_path=None, score_threshold=0.7, entropy=0.3):
        """
        Initialize the Hephaestus engine.
        
        Args:
            n_variants: Number of variants to generate per task
            registry_path: Path to the registry
            score_threshold: Minimum score for a build to be considered successful
            entropy: Entropy level for mutations (0.0-1.0)
        """
        self.forge_loop = ForgeLoop(
            n_variants=n_variants,
            registry_path=registry_path,
            score_threshold=score_threshold,
            entropy=entropy
        )
        self.logger = logging.getLogger("HephaestusEngine")
    
    def run(self, max_iterations=None, emergency_stop_path="emergency_stop.flag"):
        """
        Run the Hephaestus engine.
        
        Args:
            max_iterations: Maximum number of iterations
            emergency_stop_path: Path to emergency stop flag file
            
        Returns:
            Final state of the shared data store
        """
        self.forge_loop.max_iterations = max_iterations
        self.forge_loop.emergency_stop_path = emergency_stop_path
        
        self.logger.info("Starting Hephaestus Engine")
        
        # Initial shared state
        shared = {}
        
        # Run the forge loop
        final_state = self.forge_loop.run_forge(shared)
        
        self.logger.info("Hephaestus Engine completed")
        return final_state

def main():
    """
    Main entry point for running Hephaestus.
    """
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Hephaestus Self-Improving System")
    parser.add_argument("--iterations", type=int, default=None, help="Maximum number of iterations")
    parser.add_argument("--variants", type=int, default=3, help="Number of variants per task")
    parser.add_argument("--registry", type=str, default=None, help="Path to registry directory")
    parser.add_argument("--stop-file", type=str, default="emergency_stop.flag", help="Path to emergency stop flag file")
    parser.add_argument("--entropy", type=float, default=0.3, help="Entropy level for mutations (0.0-1.0)")
    parser.add_argument("--score-threshold", type=float, default=0.7, help="Minimum score for success")
    
    args = parser.parse_args()
    
    # Create and run the engine
    engine = HephaestusEngine(
        n_variants=args.variants,
        registry_path=args.registry,
        score_threshold=args.score_threshold,
        entropy=args.entropy
    )
    
    engine.run(
        max_iterations=args.iterations,
        emergency_stop_path=args.stop_file
    )

if __name__ == "__main__":
    main()
