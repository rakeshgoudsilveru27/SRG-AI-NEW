"""
=========================================================
SRG AI - Wikipedia Service
=========================================================
Handles Wikipedia search and summaries.
"""

import requests

from backend.utils.logger import logger


class WikipediaService:

    SEARCH_URL = "https://en.wikipedia.org/w/api.php"

    USER_AGENT = {
        "User-Agent": "SRG-AI/2.0"
    }

    @staticmethod
    def get_summary(query):
        """
        Search Wikipedia and return a short summary.
        Returns None if no page is found.
        """

        if not query or not query.strip():
            return None

        try:

            logger.info(f"Searching Wikipedia: {query}")

            # --------------------------------------------
            # Search Wikipedia
            # --------------------------------------------

            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json"
            }

            response = requests.get(
                WikipediaService.SEARCH_URL,
                params=params,
                headers=WikipediaService.USER_AGENT,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            results = (
                data.get("query", {})
                    .get("search", [])
            )

            if not results:

                logger.info("No Wikipedia article found.")

                return None

            page_title = results[0]["title"]

            # --------------------------------------------
            # Get Page Summary
            # --------------------------------------------

            summary_url = (
                "https://en.wikipedia.org/api/rest_v1/page/summary/"
                + page_title.replace(" ", "_")
            )

            summary_response = requests.get(
                summary_url,
                headers=WikipediaService.USER_AGENT,
                timeout=10
            )

            summary_response.raise_for_status()

            summary_data = summary_response.json()

            summary = summary_data.get("extract")

            if not summary:

                logger.info("Wikipedia summary unavailable.")

                return None

            logger.info(f"Wikipedia summary found: {page_title}")

            return (
                f"📚 Wikipedia\n\n"
                f"📖 Title: {page_title}\n\n"
                f"{summary}"
            )

        except requests.exceptions.Timeout:

            logger.error("Wikipedia request timed out.")

            return None

        except requests.exceptions.RequestException as e:

            logger.error(str(e))

            return None

        except Exception:

            logger.exception("Wikipedia Service Error")

            return None