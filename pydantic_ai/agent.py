from __future__ import annotations as _annotations

from typing import Any, Callable, Generic, Sequence, overload

from . import function_calls as fc
from .function_calls import AgentContext
from .result import ResponseType, RunResult, RunStreamResult


class Agent(Generic[ResponseType, AgentContext]):
    """Main class for creating "agents" - a way to have a specific type of "conversation" with an LLM."""

    def __init__(
        self,
        system_prompt: str | Sequence[str] = '',
        response_type: type[ResponseType] = str,
        context: AgentContext = None,
    ):
        self._system_prompt = system_prompt
        self._system_prompt_functions: list[Any] = []
        self._response_type = response_type
        self._context = context

    def run(self, user_prompt: str) -> RunResult[ResponseType]:
        """Run the agent with a user prompt."""
        raise NotImplementedError()

    async def async_run(self, user_prompt: str) -> RunResult[ResponseType]:
        """Run the agent with a user prompt asynchronously."""
        raise NotImplementedError()

    def stream(self, user_prompt: str) -> RunStreamResult[ResponseType]:
        """Run the agent with a user prompt and stream the results."""
        raise NotImplementedError()

    async def async_stream(self, user_prompt: str) -> RunStreamResult[ResponseType]:
        """Run the agent with a user prompt asynchronously and stream the results."""
        raise NotImplementedError()

    def system_prompt(self, func: fc.SystemPrompt[AgentContext]) -> fc.SystemPrompt[AgentContext]:
        """Decorator to register a system prompt function."""
        self._system_prompt_functions.append(func)
        return func

    @overload
    def retriever(self, func: fc.Retriever[AgentContext, fc.P, fc.R], /) -> fc.Retriever[AgentContext, fc.P, fc.R]: ...

    @overload
    def retriever(
        self, /, *, retries: int = 0
    ) -> Callable[
        [fc.Retriever[AgentContext, fc.P, fc.R]],
        fc.Retriever[AgentContext, fc.P, fc.R],
    ]: ...

    def retriever(self, func: fc.Retriever[AgentContext, fc.P, fc.R] | None = None, /, *, retries: int = 0) -> Any:
        """Decorator to register a retriever function."""
        if func is None:

            def retriever_decorator(
                func_: fc.Retriever[AgentContext, fc.P, fc.R],
            ) -> fc.Retriever[AgentContext, fc.P, fc.R]:
                self._register_retriever(func_, retries)
                return func_

            return retriever_decorator
        else:
            self._register_retriever(func, retries)
            return func

    def _register_retriever(self, func: fc.Retriever[AgentContext, fc.P, fc.R], retries: int) -> None:
        pass
