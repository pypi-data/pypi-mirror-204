from __future__ import annotations

import inspect
from typing import Any, Callable, Iterator, Protocol, Sequence

from rapidfuzz.distance import Indel

__all__ = ["menu", "Ask", "Tell"]

Ask = Callable[[str], str]

Tell = Callable[[str], None]

ActionCallback = Callable[..., Any]


class NormalizedActionCallback(Protocol):
    def __call__(self, state: Any, ask: Ask, tell: Tell) -> Any:
        """
        A callback that represents an action in the menu.

        :param state: Initial state data before performing the action.
        :param ask: A function that queries the user for input.
        :param tell: A function that provides feedback or information to the user.

        :return: The new state data after performing the action.
        """
        ...


def similarity(s1: str, s2: str) -> float:
    """
    Find the normalized Indel similarity between two strings.

    :param s1: The first string to compute the similarity.
    :param s2: The second string to compute the similarity.
    :return: The normalized Indel similarity value between s1 and s2.
    """
    return Indel.normalized_similarity(s1, s2)


class NextProtocol(Protocol):
    def next(self, state: Any, ask: Ask, tell: Tell) -> tuple[Menu | Action | None, Any]:
        ...


class Menu(NextProtocol):
    def __init__(
        self,
        parent: Menu | None = None,
    ) -> None:
        """
        Initialize a Menu object.

        :param parent: Optional parent menu. Default is None, for top level menu.
        """
        self._items: list[tuple[str, Menu | Action]] = []
        self.parent: Menu | None = parent
        self.callback: NormalizedActionCallback | None = None

    @property
    def _items_list(self) -> Sequence[tuple[str, Menu | Action | None]]:
        items: list[tuple[str, Menu | Action | None]] = list(self._items)
        if (parent := self.parent) is not None:
            items.append(("Return to previous menu", parent))
        else:
            items.append(("Exit", None))
        return items

    @property
    def _menu(self) -> Iterator[str]:
        for i, item in enumerate(self._items_list):
            yield f"{i + 1}. {item[0]}"

    def _get_item(self, name: str) -> Menu | Action | None:
        """
        Get an item from the list of items by matching its name or index using a similarity function.

        This function takes a name and tries to find the most similar name or index in the list
        of items. If the similarity match is 50% (0.5) or greater, the corresponding item is returned.

        :param name: The name or index of the item to be matched.
        :return: The matched item, which can be a Menu, Action, or None.
        :raises KeyError: If the name cannot be matched to an item with a minimum similarity of 0.5.
        """

        # Calculate the similarity ratio for each item name, and find the max similarity
        max_ratio, item = max((similarity(x[0].lower(), name.lower()), x) for x in self._items_list)

        if max_ratio >= 0.5:
            # Return the item if the max similarity ratio is 50% or higher
            return item[1]

        # If the name is not similar to any item names, try matching the index instead
        max_ratio, index = max(
            (similarity(str(i), name), i) for i, _ in enumerate(self._items_list, 1)
        )

        if max_ratio >= 0.5:
            # Return the item if the index match is 50% or higher
            return self._items_list[index - 1][1]

        # Raise a KeyError if no match is found with a minimum similarity of 0.5
        raise KeyError(name)

    def __call__(self, callback: ActionCallback) -> Menu:
        """
        Turns the menu into a decorator for the callback function.

        :param callback: A function to be executed when the corresponding action is triggered in
                         the menu.
        :return: The menu instance with the callback assigned (self).

        Usage::


            menu = Menu()

            @menu.menu("First Submenu")
            def first_submenu(state: dict) -> dict:
                # here goes the code that runs when you enter the submenu
                ...
        """
        # Normalize the input callback and store it, or set it to None if not provided
        self.callback = normalize_callback(callback) if callback is not None else None

        # Return the instance so that this method can be used in a fluent API style
        return self

    def menu(self, name: str) -> Menu:
        """
        Creates a new submenu with the given name and adds it as an item to the current menu.

        :param name: The name of the submenu to be added.
        :return: The created submenu.
        """
        # Create a new submenu with the current menu as its parent
        submenu = Menu(parent=self)

        # Append the submenu with its name to the list of items of the current menu
        self._items.append((name, submenu))
        return submenu

    def action(self, name: str) -> Action:
        """
        Add an action with the given name to the parent object.

        :param name: A string representing the name of the action.
        :return: An instance of the Action class.
        """

        # Create a new instance of the Action class and set its parent to the current object
        action = Action(parent=self)

        # Add a tuple consisting of the action name and action instance to the _items list
        self._items.append((name, action))

        return action

    def next(
        self,
        state: Any,
        ask: Ask,
        tell: Tell,
    ) -> tuple[Menu | Action | None, Any]:
        """
        Update and generate the next menu or action given the input state.

        :param state: The current state of the menu interactions.
        :param ask: A function to ask a question and get user's input.
        :param tell: A function to display text to the user.
        :return: A tuple containing the next menu or action, and the updated state.
        """
        if (callback := self.callback) is not None:
            state = callback(state, ask, tell)
        question = "Please select an option:\n" + "\n".join(self._menu)
        while True:
            question_answer = ask(question)
            try:
                return self._get_item(question_answer), state
            except KeyError:
                question = "Invalid option, please try again."

    def communicate(self, state: Any, ask: Ask, tell: Tell) -> None:
        """
        Handle the menu communication with the user.

        :param state: The current state of the menu interactions.
        :param ask: A function to ask a question and get user's input.
        :param tell: A function to display text to the user.
        """
        current: Menu | Action | None = self
        while current is not None:
            current, state = current.next(state, ask, tell)


def menu() -> Menu:
    """
    Create a new instance of the Menu class and return it.

    :return: An instance of the Menu class.
    """
    return Menu()


class Action(NextProtocol):
    def __init__(
        self,
        parent: Menu,
    ) -> None:
        """
        Initialize an Action object.

        :param parent: The parent menu of this action.
        """
        self.parent = parent
        self.callback: NormalizedActionCallback | None = None

    def next(
        self,
        state: Any,
        ask: Ask,
        tell: Tell,
    ) -> tuple[Menu, Any]:
        """
        Update and generate the next menu or action given the current state.

        :param state: The current state of the user interaction.
        :param ask: A function to ask a question and get user's input.
        :param tell: A function to display text to the user.
        :return: A tuple containing the next menu or action, and the updated state.
        """
        if (callback := self.callback) is not None:
            state = callback(state, ask=ask, tell=tell)
        return self.parent, state

    def __call__(self, callback: ActionCallback) -> Action:
        """
        Turns the action into a decorator for the callback function.

        :param callback: The callback function to be executed when the action is triggered.
        :return: The instance itself, allowing for chainable method calls.
        :raises: ValueError if the provided callback is not None and does not conform to the
            required ActionCallback signature.
        """
        # Normalize the callback if it's not None, otherwise simply set it to None.
        self.callback = normalize_callback(callback) if callback is not None else None

        # Return the instance itself for chaining.
        return self


def normalize_callback(callback: ActionCallback) -> NormalizedActionCallback:
    """
    Normalize a callback to match the required (state, ask, tell) arguments.

    :param callback: The callback to normalize.
    :return: A normalized callback with (state, ask, tell) arguments.
    :raise ValueError: If given callback has an unsupported signature.
    """
    signature = inspect.signature(callback)
    parameters = signature.parameters
    if len(parameters) == 3:
        # def callback(state: Any, ask: Ask, tell: Tell) -> Any:
        return callback
    elif len(parameters) == 2:
        if "ask" in parameters and "tell" not in parameters:
            # def callback(state: Any, ask: Ask) -> Any:
            return lambda state, ask, tell: callback(state, ask=ask)
        elif "ask" not in parameters and "tell" in parameters:
            # def callback(state: Any, tell: Tell) -> Any:
            return lambda state, ask, tell: callback(state, tell=tell)
        elif "ask" in parameters and "tell" in parameters:
            # def callback(ask: Ask, tell: Tell) -> Any:
            return lambda state, ask, tell: callback(ask=ask, tell=tell)
        else:
            raise ValueError("wrong callback signature")
    elif len(parameters) == 1:
        if "ask" in parameters:
            # def callback(ask: Ask) -> Any:
            return lambda state, ask, tell: callback(ask=ask)
        elif "tell" in parameters:
            # def callback(tell: Tell) -> Any:
            return lambda state, ask, tell: callback(tell=tell)
        else:
            # def callback(state: Any) -> Any:
            return lambda state, ask, tell: callback(state)
    elif len(parameters) == 0:
        # def callback() -> Any:
        return lambda state, ask, tell: callback()
    else:
        raise ValueError("wrong callback signature")
