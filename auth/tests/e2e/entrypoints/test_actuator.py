"""
Test Actuator entry point
"""
from fastapi import status


class TestActuator:

    def test_api_root_redirects_to_docs(self, test_client):
        """
        Tests that the root path redirects to the docs.
        """
        response = test_client.get("/").history[0]
        assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY
        assert response.headers["location"] == "/docs"

    def test_health_check(self, test_client):
        """
        Tests that the health check endpoint returns 200.
        """
        response = test_client.get("/liveliness")
        assert response.status_code == status.HTTP_200_OK
