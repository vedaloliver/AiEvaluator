"""Client for communicating with the Observability Service."""

import logging
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger(__name__)


class ObservabilityClient:
    """Client for sending observability data to the centralized service."""

    def __init__(self, base_url: str):
        """
        Initialize the observability client.

        Args:
            base_url: Base URL of the observability service (e.g., http://localhost:8003)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = 5.0  # 5 second timeout

    async def create_trace(self, trace_id: str) -> bool:
        """
        Create a new trace.

        Args:
            trace_id: Unique trace identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/traces",
                    json={"traceId": trace_id}
                )
                response.raise_for_status()
                logger.info(f"Created trace: {trace_id}")
                return True
        except httpx.HTTPError as e:
            logger.error(f"Error creating trace: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating trace: {e}")
            return False

    async def create_span(self, span_data: Dict[str, Any]) -> bool:
        """
        Create a new span.

        Args:
            span_data: Span data (spanId, traceId, name, spanType, etc.)

        Returns:
            True if successful, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/spans",
                    json=span_data
                )
                response.raise_for_status()
                logger.info(f"Created span: {span_data.get('spanId')}")
                return True
        except httpx.HTTPError as e:
            logger.error(f"Error creating span: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating span: {e}")
            return False

    async def store_evaluation_run(self, eval_data: Dict[str, Any]) -> Optional[int]:
        """
        Store an evaluation run.

        Args:
            eval_data: Evaluation run data

        Returns:
            Run ID if successful, None otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/evaluation-runs",
                    json=eval_data
                )
                response.raise_for_status()
                result = response.json()
                run_id = result.get("id")
                logger.info(f"Stored evaluation run: {run_id}")
                return run_id
        except httpx.HTTPError as e:
            logger.error(f"Error storing evaluation run: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error storing evaluation run: {e}")
            return None

    async def update_trace(self, trace_id: str, status: str = "completed") -> bool:
        """
        Update a trace status.

        Args:
            trace_id: Trace identifier
            status: New status (default: "completed")

        Returns:
            True if successful, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.patch(
                    f"{self.base_url}/api/v1/traces/{trace_id}",
                    json={"status": status}
                )
                response.raise_for_status()
                logger.info(f"Updated trace {trace_id} to status: {status}")
                return True
        except httpx.HTTPError as e:
            logger.error(f"Error updating trace: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error updating trace: {e}")
            return False
