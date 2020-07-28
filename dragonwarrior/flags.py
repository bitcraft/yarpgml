from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ActionToken:
    label: str
    initial: Optional[List[str]]
    final: str
    replace: bool = False


@dataclass
class Action:
    initial: int
    final: int
    edge: str
    replace: bool = False


class Resolver:

    def __init__(self):
        self._actions = list()
        self._raw_flags = list()
        self._flags = list()
        self._flags_by_name = dict()
        self._flags_by_value = dict()
        self._valid_states = set()

    def actions(self) -> List[Action]:
        return self._actions

    def add_action_tokens(self, actions: List[ActionToken]):
        for action in actions:
            self.add_action_token(action)

    def add_action_token(self, action_token: ActionToken):
        self.add_flag(action_token.final)
        if action_token.initial is None:
            initial = 0
        else:
            self.add_flags(action_token.initial)
            initial = self.get_value_of_flags(action_token.initial)
        action = Action(
            initial=initial,
            final=self.get_value_of_flag(action_token.final),
            edge=action_token.label,
            replace=action_token.replace,
        )
        self.add_action(action)

    def add_action(self, action: Action):
        self._actions.append(action)

    def add_flags(self, flags: List[str]):
        for flag in flags:
            self.add_flag(flag)

    def add_flag(self, flag: str):
        if flag not in self._raw_flags:
            self._raw_flags.append(flag)
            self.update_flags()

    def get_value_of_flag(self, flag: str):
        return self._flags_by_name[flag]

    def get_value_of_flags(self, flags: List[str]):
        return sum(self.get_value_of_flag(i) for i in flags)

    def update_flags(self):
        flags = [(pow(2, i), v) for i, v in enumerate(self._raw_flags)]
        self._flags = flags
        self._flags_by_value = dict(flags)
        self._flags_by_name = dict((v, k) for k, v in flags)

    def update_valid_states(self):
        self._valid_states = set()
        for action in self.actions():
            self._valid_states.add(action.initial)
            if action.replace:
                self._valid_states.add(action.final)
            else:
                self._valid_states.add(action.initial | action.final)
        print(sorted(self._valid_states))

    def state_names_in_value(self, value):
        names = []
        for flag_value, flag_name in self._flags:
            if value & flag_value == flag_value:
                names.append(flag_name)
        names.sort()
        return " ".join(names)

    def run(self):
        quest_log = 0

        with open("test.dot", "w") as fp:
            used_nodes = set()
            fp.write('digraph G {\ngraph [compound=true rankdir="LR"]\n')
            # for state in range((max(self._valid_states) * 2)):
            self.update_valid_states()
            for state in self._valid_states:
                for action in self.actions():
                    # flip the initial flags
                    if action.replace:
                        dest = state ^ action.initial
                        dest = dest ^ action.final
                    else:
                        dest = state ^ action.final
                    # flip the final flags
                    # does this state satisfy the initial?
                    test1 = state & action.initial == action.initial
                    # does the state already satisfy the final?
                    test2 = not (state & action.final == action.final)
                    # has this action already been done?
                    test3 = not (quest_log & action.final == action.final)
                    # print(state, test1, test2, test3, action, dest)
                    test4 = dest in self._valid_states
                    if test1 and test2 and test3 and test4:
                        # record the quest
                        quest_log = quest_log ^ action.final
                        used_nodes.add(state)
                        used_nodes.add(dest)
                        fp.write(f"\"{state}\" -> {dest:<6} [label=\"{action.edge}\"]\n")

            for state in used_nodes:
                node_label = str(state) + ": " + self.state_names_in_value(state)
                fp.write(f"{state} [label=\"{node_label}\"]\n")

            fp.write("}\n")


if __name__ == "__main__":
    all_actions = [
        ActionToken("rescue princess", ["begin"], "princess1"),
        ActionToken("get harp", ["begin"], "harp"),
        ActionToken("get stones", ["begin"], "stones"),
        ActionToken("get token", ["begin"], "token"),
        ActionToken("swap for staff", ["harp"], "staff"),
        ActionToken("swap for drop", ["staff", "stones", "token"], "drop"),
        ActionToken("swap for bridge", ["drop"], "bridge"),
        ActionToken("join dragonlord", ["bridge"], "join"),
        ActionToken("defeat dragonlord", ["bridge"], "defeat"),
        ActionToken("rescue princess", ["defeat"], "princess2"),
        ActionToken("restore peace1", ["defeat"], "peace1"),
        ActionToken("restore peace2", ["princess2"], "peace2"),
    ]
    r = Resolver()
    r.add_action_tokens(all_actions)
    r.run()
