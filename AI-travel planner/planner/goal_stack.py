class Action:
    def __init__(self, name, preconditions, add_effects, delete_effects):
        self.name = name
        self.preconditions = set(preconditions)
        self.add_effects = set(add_effects)
        self.delete_effects = set(delete_effects)

    def apply(self, state):
        return (state - self.delete_effects) | self.add_effects


class GoalStackPlanner:
    def __init__(self, actions):
        self.actions = actions

    def select_action(self, goal):
        for action in self.actions:
            if goal in action.add_effects:
                return action
        raise ValueError(f"No action can achieve goal: {goal}")

    def plan(self, initial_state, goal_state):
        state = set(initial_state)
        stack = [set(goal_state)]
        plan = []

        while stack:
            item = stack.pop()

            if isinstance(item, set):
                missing_goals = [goal for goal in item if goal not in state]
                if missing_goals:
                    stack.append(item)
                    for goal in reversed(missing_goals):
                        stack.append(goal)
                continue

            if isinstance(item, str):
                if item in state:
                    continue
                action = self.select_action(item)
                stack.append(action)
                stack.append(set(action.preconditions))
                continue

            if item.preconditions.issubset(state):
                state = item.apply(state)
                plan.append(item.name)
                continue

            stack.append(item)
            stack.append(set(item.preconditions))

        return plan
