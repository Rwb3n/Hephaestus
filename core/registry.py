"""
Hephaestus Core Registry Module

This module contains the Registry class responsible for managing
persistent storage of build artifacts, tracking lineage, and
providing querying capabilities for the build database.
"""

import os
import json
import uuid
import time
import logging
from typing import Dict, List, Any, Optional, Union, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Registry:
    """
    Registry manages the persistent storage of build artifacts and lineage.
    
    It provides methods for:
    - Recording new builds
    - Retrieving past builds
    - Tracking lineage and ancestry
    - Querying the build database
    
    The Registry stores build metadata in an index file and full build
    details in individual JSON files within a builds directory.
    """
    
    def __init__(self, registry_path: str = None):
        """
        Initialize the Registry.
        
        Args:
            registry_path: Path to the registry directory
        """
        self.registry_path = registry_path or os.path.dirname(__file__)
        self.logger = logging.getLogger("Registry")
        
        # Create registry directory structure if it doesn't exist
        os.makedirs(os.path.join(self.registry_path, "builds"), exist_ok=True)
        
        # Load or initialize the registry index
        self.registry_file = os.path.join(self.registry_path, "registry.json")
        self._load_index()
    
    def _load_index(self) -> None:
        """Load the registry index from disk or initialize a new one."""
        try:
            if os.path.exists(self.registry_file):
                with open(self.registry_file, 'r') as f:
                    self.index = json.load(f)
            else:
                self.index = {
                    "builds": [],
                    "lineage": {},
                    "last_build_id": 0
                }
                self._save_index()
        except Exception as e:
            self.logger.error(f"Failed to load registry index: {str(e)}")
            # Initialize with empty state as a fallback
            self.index = {
                "builds": [],
                "lineage": {},
                "last_build_id": 0
            }
    
    def _save_index(self) -> None:
        """Save the registry index to disk."""
        try:
            # Write to a temporary file first to ensure atomic update
            temp_file = f"{self.registry_file}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(self.index, f, indent=2)
            
            # Then rename to the actual file (atomic on most file systems)
            os.replace(temp_file, self.registry_file)
        except Exception as e:
            self.logger.error(f"Failed to save registry index: {str(e)}")
    
    def record_build(self, entry: Dict[str, Any]) -> str:
        """
        Record a new build in the registry.
        
        Args:
            entry: A dictionary containing build information with these keys:
                - build_task: The original task description
                - directive: The directive used to generate the code
                - code: The generated code
                - test_results: Results from the test harness
                - score: The normalized score (0-1)
                - parent_id: The ID of the parent build (if any)
                - imports: List of imports used
                - status: "success" or "fail"
                
        Returns:
            The UUID of the new build entry
        """
        # Generate a unique build ID
        build_id = str(uuid.uuid4())
        
        # Add metadata to the entry
        entry["build_id"] = build_id
        entry["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Ensure all required fields exist with defaults
        entry.setdefault("parent_id", None)
        entry.setdefault("status", "unknown")
        entry.setdefault("score", 0.0)
        entry.setdefault("imports", [])
        
        # Save the full build entry to a file
        build_file = os.path.join(self.registry_path, "builds", f"{build_id}.json")
        try:
            with open(build_file, 'w') as f:
                json.dump(entry, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save build file {build_id}: {str(e)}")
            return None
        
        # Update the index with summary information
        build_summary = {
            "build_id": build_id,
            "parent_id": entry.get("parent_id"),
            "score": entry.get("score", 0.0),
            "status": entry.get("status", "unknown"),
            "timestamp": entry.get("timestamp"),
            "imports": entry.get("imports", [])
        }
        
        self.index["builds"].append(build_summary)
        
        # Update lineage tracking
        parent_id = entry.get("parent_id")
        if parent_id:
            if parent_id not in self.index["lineage"]:
                self.index["lineage"][parent_id] = []
            self.index["lineage"][parent_id].append(build_id)
        
        # Save the updated index
        self._save_index()
        
        self.logger.info(f"Recorded build {build_id} with score {entry.get('score', 0.0)}")
        return build_id
    
    def get_build(self, build_id: str) -> Dict[str, Any]:
        """
        Retrieve a build by ID.
        
        Args:
            build_id: The UUID of the build
            
        Returns:
            The full build entry or None if not found
        """
        build_file = os.path.join(self.registry_path, "builds", f"{build_id}.json")
        try:
            if os.path.exists(build_file):
                with open(build_file, 'r') as f:
                    return json.load(f)
            else:
                self.logger.warning(f"Build {build_id} not found")
                return None
        except Exception as e:
            self.logger.error(f"Failed to load build {build_id}: {str(e)}")
            return None
    
    def get_builds(self, 
                   filters: Dict[str, Any] = None, 
                   limit: int = 10, 
                   sort_by: str = "timestamp", 
                   reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Query builds with filters.
        
        Args:
            filters: Dictionary of field:value filters
            limit: Maximum number of results
            sort_by: Field to sort by
            reverse: If True, sort in descending order
            
        Returns:
            List of matching build summaries
        """
        builds = self.index["builds"]
        
        # Apply filters if provided
        if filters:
            filtered_builds = []
            for build in builds:
                match = True
                for key, value in filters.items():
                    if key not in build or build[key] != value:
                        match = False
                        break
                if match:
                    filtered_builds.append(build)
            builds = filtered_builds
        
        # Sort the results
        if sort_by in builds[0] if builds else {}:
            builds = sorted(builds, key=lambda x: x.get(sort_by), reverse=reverse)
        
        # Apply limit
        return builds[:limit]
    
    def get_descendants(self, build_id: str) -> List[str]:
        """
        Get all descendants of a build.
        
        Args:
            build_id: The build ID to find descendants for
            
        Returns:
            List of descendant build IDs
        """
        if build_id not in self.index["lineage"]:
            return []
            
        descendants = []
        
        def collect_descendants(parent_id):
            if parent_id in self.index["lineage"]:
                for child_id in self.index["lineage"][parent_id]:
                    descendants.append(child_id)
                    collect_descendants(child_id)
        
        collect_descendants(build_id)
        return descendants
    
    def get_ancestry(self, build_id: str) -> List[str]:
        """
        Get the ancestry chain for a build.
        
        Args:
            build_id: The build ID to find ancestry for
            
        Returns:
            List of build IDs in the ancestry chain, from oldest to newest
        """
        ancestry = []
        
        # Find the build in the index
        build = None
        for b in self.index["builds"]:
            if b["build_id"] == build_id:
                build = b
                break
        
        if not build:
            return ancestry
        
        # Trace back through parents
        current_id = build["parent_id"]
        while current_id:
            # Add the parent to the ancestry
            ancestry.append(current_id)
            
            # Find this parent in the index
            parent = None
            for b in self.index["builds"]:
                if b["build_id"] == current_id:
                    parent = b
                    break
            
            if not parent:
                break
            
            # Move up to the grandparent
            current_id = parent["parent_id"]
        
        # The ancestry is oldest-to-newest
        ancestry.reverse()
        return ancestry
    
    def get_lineage_depth(self, build_id: str) -> int:
        """
        Get the depth of a build's lineage (how many ancestors it has).
        
        Args:
            build_id: The build ID to find lineage depth for
            
        Returns:
            The lineage depth (0 for builds with no parents)
        """
        ancestry = self.get_ancestry(build_id)
        return len(ancestry)
    
    def query_by_imports(self, imports: List[str]) -> List[Dict[str, Any]]:
        """
        Find builds that use similar imports.
        
        Args:
            imports: List of import strings to search for
            
        Returns:
            List of build summaries with matching imports
        """
        # Simple implementation: count matching imports
        matches = []
        for build in self.index["builds"]:
            build_imports = build.get("imports", [])
            shared_imports = set(imports).intersection(set(build_imports))
            if shared_imports:
                # Calculate similarity score as percentage of matches
                similarity = len(shared_imports) / len(imports)
                matches.append((build, similarity))
        
        # Return builds sorted by similarity
        return [build for build, similarity in sorted(matches, key=lambda x: x[1], reverse=True)]
    
    def get_top_builds(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the top N highest-scoring builds.
        
        Args:
            n: Number of builds to return
            
        Returns:
            List of build summaries
        """
        builds = sorted(self.index["builds"], key=lambda x: x.get("score", 0.0), reverse=True)
        return builds[:n]
    
    def get_recent_builds(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the N most recent builds.
        
        Args:
            n: Number of builds to return
            
        Returns:
            List of build summaries
        """
        builds = sorted(self.index["builds"], key=lambda x: x.get("timestamp", ""), reverse=True)
        return builds[:n]
    
    def prune(self, criteria: Dict[str, Any]) -> int:
        """
        Prune builds based on criteria.
        
        Args:
            criteria: Dictionary with criteria for pruning:
                - min_score: Minimum score to keep
                - older_than: Timestamp cutoff
                - keep_top_n: Always keep top N scored builds
                
        Returns:
            Number of builds pruned
        """
        min_score = criteria.get("min_score", 0.0)
        older_than = criteria.get("older_than")
        keep_top_n = criteria.get("keep_top_n")
        
        # Get top N builds to always keep
        keep_ids = set()
        if keep_top_n:
            top_builds = self.get_top_builds(n=keep_top_n)
            keep_ids = {b["build_id"] for b in top_builds}
        
        # Identify builds to prune
        to_prune = []
        for build in self.index["builds"]:
            # Skip if in the keep list
            if build["build_id"] in keep_ids:
                continue
                
            # Check score criteria
            if build.get("score", 0.0) < min_score:
                to_prune.append(build["build_id"])
                continue
                
            # Check age criteria
            if older_than and build.get("timestamp", "") < older_than:
                to_prune.append(build["build_id"])
        
        # Prune builds
        for build_id in to_prune:
            # Remove from index
            self.index["builds"] = [b for b in self.index["builds"] if b["build_id"] != build_id]
            
            # Remove its descendant relationships
            if build_id in self.index["lineage"]:
                del self.index["lineage"][build_id]
            
            # Remove from parent's lineage
            for parent_id, children in self.index["lineage"].items():
                if build_id in children:
                    self.index["lineage"][parent_id] = [c for c in children if c != build_id]
            
            # Delete the build file
            build_file = os.path.join(self.registry_path, "builds", f"{build_id}.json")
            if os.path.exists(build_file):
                os.remove(build_file)
        
        # Save the updated index
        self._save_index()
        
        self.logger.info(f"Pruned {len(to_prune)} builds")
        return len(to_prune) 