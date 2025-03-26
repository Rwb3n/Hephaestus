#!/usr/bin/env python
"""
Hephaestus - A Self-Improving Code Generation System

Hephaestus is a recursive execution engine that proposes, builds, tests, scores, and improves
its own components through an evolutionary process.

Usage:
    python run.py [--iterations N] [--variants N] [--registry PATH] [--stop-file PATH]
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from engine.forge_loop import HephaestusEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("hephaestus.log")
    ]
)

logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for Hephaestus.
    
    Parses command line arguments and initializes the system.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Hephaestus Self-Improving System")
    parser.add_argument("--iterations", type=int, 
                        default=int(os.getenv("MAX_ITERATIONS", 0)) or None, 
                        help="Maximum number of iterations")
    parser.add_argument("--variants", type=int, 
                        default=int(os.getenv("VARIANTS_PER_TASK", 3)), 
                        help="Number of variants per task")
    parser.add_argument("--registry", type=str, 
                        default=os.getenv("REGISTRY_PATH"), 
                        help="Path to registry directory")
    parser.add_argument("--stop-file", type=str, 
                        default="emergency_stop.flag", 
                        help="Path to emergency stop flag file")
    parser.add_argument("--log-level", type=str, 
                        default=os.getenv("LOG_LEVEL", "INFO"), 
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                        help="Logging level")
    parser.add_argument("--entropy", type=float,
                        default=float(os.getenv("ENTROPY_LEVEL", 0.3)),
                        help="Entropy level for mutations (0.0-1.0)")
    parser.add_argument("--score-threshold", type=float,
                        default=float(os.getenv("SCORE_THRESHOLD", 0.7)),
                        help="Minimum score for a build to be considered successful")
    
    args = parser.parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    logger.info("Initializing Hephaestus")
    logger.info(f"Configuration: iterations={args.iterations}, variants={args.variants}, entropy={args.entropy}")
    
    # Check if emergency stop already exists and clear it
    if os.path.exists(args.stop_file):
        logger.info(f"Removing existing emergency stop file: {args.stop_file}")
        os.remove(args.stop_file)
    
    try:
        # Create and run the engine
        engine = HephaestusEngine(
            n_variants=args.variants,
            registry_path=args.registry,
            score_threshold=args.score_threshold,
            entropy=args.entropy
        )
        
        result = engine.run(
            max_iterations=args.iterations,
            emergency_stop_path=args.stop_file
        )
        
        logger.info("Hephaestus completed successfully")
        return 0
    
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Exiting.")
        return 1
    
    except Exception as e:
        logger.error(f"Error running Hephaestus: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
