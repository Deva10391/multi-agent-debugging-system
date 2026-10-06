from langgraph.graph import StateGraph, END
from state import BugState
from agents.planner import planner_node
from agents.executor import executor_node
from agents.critic import critic_node

def route_after_critic(state: BugState) -> str:
    decision = state.get("critic_decision")
    if decision == "retry":
        return "planner"
    return END

def build_graph():
    graph = StateGraph(BugState)

    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "critic")
    graph.add_conditional_edges("critic", route_after_critic)

    return graph.compile()

"""
to loop 'planner executor critic' functionalities
"""