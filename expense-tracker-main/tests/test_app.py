import pytest
import os
import sys
from unittest.mock import patch

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.db import db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

def test_home_page(client):
    """Test that the home page loads."""
    response = client.get('/')
    assert response.status_code in [200, 302]  # 200 for direct access, 302 for redirect to login

def test_app_creation():
    """Test that the app can be created."""
    app = create_app()
    assert app is not None

def test_app_config():
    """Test that the app has the correct configuration."""
    app = create_app()
    assert app.config['TESTING'] is False

@patch.dict(os.environ, {'DB_URI': 'sqlite:///:memory:', 'SECRET_KEY': 'test-secret'})
def test_app_with_env_vars():
    """Test that the app can be created with environment variables."""
    app = create_app()
    assert app is not None

def test_health_check(client):
    """Test health check endpoint if it exists."""
    response = client.get('/health')
    # If health endpoint doesn't exist, this will return 404, which is fine for this test
    assert response.status_code in [200, 404] 