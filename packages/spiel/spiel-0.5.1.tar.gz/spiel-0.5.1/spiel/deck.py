from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Type, overload

from spiel.slide import Content, Slide
from spiel.transitions.protocol import Transition
from spiel.transitions.swipe import Swipe


@dataclass
class Deck(Sequence[Slide]):
    """
    Represents a "deck" of "slides": a presentation.
    """

    name: str
    """The name of the [`Deck`][spiel.Deck], which will be displayed in the footer."""

    default_transition: Type[Transition] | None = Swipe
    """\
    The default slide transition animation;
    used if the slide being moved to does not specify its own transition.
    Defaults to the [`Swipe`][spiel.Swipe] transition.
    Set to `None` for no transition animation.
    """

    _slides: list[Slide] = field(default_factory=list)

    def slide(
        self,
        title: str = "",
        bindings: Mapping[str, Callable[..., None]] | None = None,
        transition: Type[Transition] | None = None,
    ) -> Callable[[Content], Content]:
        """
        A decorator that creates a new slide in the deck,
        with the decorated function as the [`Slide.content`][spiel.Slide.content].

        Args:
            title: The title to display for the slide.
            bindings: A mapping of
                [keys](https://textual.textualize.io/guide/input/#key)
                to callables to be executed when those keys are pressed,
                when on this slide.
            transition: The transition animation to use when moving to this slide.
                Set to `None` to use the
                [`Deck.default_transition`][spiel.Deck.default_transition]
                of the deck this slide is in.
        """

        def slideify(content: Content) -> Content:
            self.add_slides(
                Slide(
                    title=title,
                    content=content,
                    bindings=bindings or {},
                    transition=transition,
                )
            )
            return content

        return slideify

    def add_slides(self, *slides: Slide) -> None:
        """
        Add `Slide`s to a `Deck`.

        This function is primarily useful when adding multiple slides at once,
        probably generated programmatically.
        If adding a single slide, prefer the [`Deck.slide`][spiel.Deck.slide] decorator.

        Args:
            *slides: The `Slide`s to add.
        """
        self._slides.extend(slides)

    def __len__(self) -> int:
        return len(self._slides)

    @overload
    def __getitem__(self, item: int) -> Slide:
        return self._slides[item]

    @overload
    def __getitem__(self, item: slice) -> Sequence[Slide]:
        return self._slides[item]

    def __getitem__(self, item: int | slice) -> Slide | Sequence[Slide]:
        return self._slides[item]

    def __iter__(self) -> Iterator[Slide]:
        yield from self._slides

    def __contains__(self, item: object) -> bool:
        return item in self._slides
