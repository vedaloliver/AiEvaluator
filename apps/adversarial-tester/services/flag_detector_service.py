"""Detect critical flags in LLM responses using pattern matching

This service analyzes LLM responses for critical safety violations
using regex patterns and keyword matching.
"""
import re
from typing import List, Dict
from config.critical_flags import FCA_CRITICAL_FLAGS


class SafetyFlag:
    """Represents a detected safety flag"""

    def __init__(
        self,
        flag_id: str,
        name: str,
        severity: str,
        detected: bool,
        context: str = None,
        matched_pattern: str = None
    ):
        self.flag_id = flag_id
        self.name = name
        self.severity = severity
        self.detected = detected
        self.context = context
        self.matched_pattern = matched_pattern

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "flagId": self.flag_id,
            "name": self.name,
            "severity": self.severity,
            "detected": self.detected,
            "context": self.context,
            "matchedPattern": self.matched_pattern
        }


class FlagDetectorService:
    """Detects critical flags using keyword and pattern matching"""

    def __init__(self):
        self.flag_definitions = FCA_CRITICAL_FLAGS

    def detect_flags(self, response: str) -> List[SafetyFlag]:
        """
        Check response for critical flag patterns

        Args:
            response: LLM response text to analyze

        Returns:
            List of detected SafetyFlag objects
        """
        detected = []

        for flag_id, flag_config in self.flag_definitions.items():
            flag = self._check_flag(flag_id, flag_config, response)
            if flag:
                detected.append(flag)

        return detected

    def _check_flag(
        self,
        flag_id: str,
        flag_config: Dict,
        response: str
    ) -> SafetyFlag | None:
        """
        Check if a specific flag is present in the response

        Args:
            flag_id: Identifier for the flag
            flag_config: Configuration dict with patterns and metadata
            response: Response text to check

        Returns:
            SafetyFlag if detected, None otherwise
        """
        patterns = flag_config.get("patterns", [])

        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                # Extract context around the match
                start = max(0, match.start() - 20)
                end = min(len(response), match.end() + 20)
                context = response[start:end].strip()

                return SafetyFlag(
                    flag_id=flag_id,
                    name=flag_config.get("name", flag_id),
                    severity=flag_config.get("severity", "high"),
                    detected=True,
                    context=context,
                    matched_pattern=pattern
                )

        return None

    def check_specific_flags(
        self,
        response: str,
        flag_ids: List[str]
    ) -> List[SafetyFlag]:
        """
        Check for specific flags only

        Args:
            response: Response text to analyze
            flag_ids: List of flag IDs to check for

        Returns:
            List of detected SafetyFlag objects
        """
        detected = []

        for flag_id in flag_ids:
            if flag_id in self.flag_definitions:
                flag = self._check_flag(
                    flag_id,
                    self.flag_definitions[flag_id],
                    response
                )
                if flag:
                    detected.append(flag)

        return detected

    def get_flag_definition(self, flag_id: str) -> Dict | None:
        """
        Get the definition for a specific flag

        Args:
            flag_id: Flag identifier

        Returns:
            Flag configuration dict or None if not found
        """
        return self.flag_definitions.get(flag_id)

    def get_all_flag_ids(self) -> List[str]:
        """
        Get list of all available flag IDs

        Returns:
            List of flag identifier strings
        """
        return list(self.flag_definitions.keys())
