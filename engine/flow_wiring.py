directive_loader = DirectiveLoader()
flow_builder = FlowBuilderNode()

directive_loader >> flow_builder

flow = Flow(start=directive_loader)

shared = {
  "build_task": "Create a Node that checks Python scripts for line count and warns if they exceed 200 lines.",
  "registry": json.load(open("heph/engine/registry.json"))
}

flow.run(shared)
json.dump(shared["registry"], open("heph/engine/registry.json", "w"), indent=2)
