# News Anchor RAG System

A modern, AI-powered personalized news broadcast system built with FastAPI, LangChain, and vector databases. This system uses Retrieval-Augmented Generation (RAG) to create personalized news summaries and audio broadcasts for users based on their preferences.

## 🚀 Features

- **Personalized News Curation**: AI-powered article selection based on user preferences
- **RAG-based Content Generation**: Intelligent summarization using retrieval-augmented generation
- **Audio Broadcast Generation**: Text-to-speech conversion for news broadcasts
- **Vector Search**: Semantic search capabilities using ChromaDB
- **Clean Architecture**: Domain-driven design with clear separation of concerns
- **Async/Await Support**: Built for high performance with async operations
- **RESTful API**: Comprehensive REST API with OpenAPI documentation
- **Background Tasks**: Celery integration for async processing
- **Comprehensive Testing**: Unit, integration, and e2e test coverage

## 🏗️ Architecture

This project follows Clean Architecture principles:

```
src/news_anchor/
├── api/                 # API layer (FastAPI routes, middleware)
├── application/         # Application layer (use cases, services, DTOs)
├── domain/             # Domain layer (entities, repositories, interfaces)
├── infrastructure/     # Infrastructure layer (external services, persistence)
├── shared/             # Shared utilities and enums
└── core/              # Core configuration and cross-cutting concerns
```

### Key Components

- **Domain Entities**: `Article`, `User`, `Broadcast`, `Preference`
- **Application Services**: `RAGService`, `SummarizerService`, `RankingService`
- **Use Cases**: `GenerateBroadcast`, `RetrieveArticles`, `UpdatePreferences`
- **Infrastructure**: Database, Vector Store, LLM Provider, TTS Provider

## 🛠️ Technology Stack

### Core Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.9+**: Modern Python with type hints and async support
- **Pydantic**: Data validation and settings management

### AI & Machine Learning
- **LangChain**: Framework for building LLM applications
- **OpenAI GPT**: Language model for content generation
- **ChromaDB**: Vector database for semantic search
- **Sentence Transformers**: Embedding generation

### Database & Storage
- **PostgreSQL**: Primary database with async support
- **Redis**: Caching and task queue backend
- **SQLAlchemy**: Modern async ORM
- **Alembic**: Database migration tool

### Audio & Content Processing
- **Text-to-Speech**: Multiple TTS provider support (OpenAI, ElevenLabs, Google)
- **Audio Processing**: PyDub for audio manipulation
- **Content Parsing**: Advanced text processing and cleaning

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12+ 
- Redis 6+
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/newsanchor/rag-system.git
   cd rag-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up the database**
   ```bash
   # Create database
   createdb news_anchor
   
   # Run migrations
   alembic upgrade head
   
   # Seed with sample data
   python scripts/seed_data.py
   ```

6. **Start the development server**
   ```bash
   uvicorn src.news_anchor.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

This will start all required services including PostgreSQL, Redis, and the application.

## ⚙️ Configuration

### Environment Variables

Key configuration options (see `.env.example` for complete list):

```bash
# Application
PROJECT_NAME="News Anchor RAG System"
ENVIRONMENT="development"
DEBUG=true

# Database
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/news_anchor"

# AI Services
OPENAI_API_KEY="your-openai-api-key"
OPENAI_MODEL="gpt-3.5-turbo"

# Vector Database
CHROMA_HOST="localhost"
CHROMA_PORT=8000

# Redis
REDIS_URL="redis://localhost:6379/0"

# TTS Provider
TTS_PROVIDER="openai"  # openai, elevenlabs, google
```

### Feature Flags

Enable/disable features via environment variables:

```bash
ENABLE_RAG_SEARCH=true
ENABLE_AUDIO_GENERATION=true
ENABLE_REAL_TIME_UPDATES=false
ENABLE_ANALYTICS=true
```

## 🚀 Usage

### API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI Schema**: http://localhost:8000/api/v1/openapi.json

### Key Endpoints

#### News & Articles
```http
GET /api/v1/news/                    # List articles
GET /api/v1/news/{article_id}        # Get specific article
POST /api/v1/news/search             # Semantic search
POST /api/v1/news/                   # Create article
```

#### Broadcasts
```http
GET /api/v1/broadcasts/              # List broadcasts
POST /api/v1/broadcasts/generate     # Generate personalized broadcast
POST /api/v1/broadcasts/{id}/audio   # Generate audio
```

#### User Preferences
```http
GET /api/v1/preferences/{user_id}    # Get user preferences
PUT /api/v1/preferences/{user_id}    # Update preferences
```

### Example Usage

#### Generate a Personalized Broadcast

```python
import httpx

# Generate broadcast
response = httpx.post("http://localhost:8000/api/v1/broadcasts/generate", json={
    "user_id": "user-123",
    "max_articles": 10,
    "broadcast_type": "daily",
    "generate_audio": true,
    "preferences": {
        "preferred_categories": ["technology", "science"],
        "keywords": ["AI", "machine learning"],
        "max_articles_per_broadcast": 10
    }
})

broadcast = response.json()
print(f"Generated broadcast: {broadcast['title']}")
```

#### Search Articles

```python
# Semantic search
response = httpx.post("http://localhost:8000/api/v1/news/search", json={
    "query": "artificial intelligence healthcare",
    "limit": 5,
    "similarity_threshold": 0.7
})

results = response.json()
for result in results["results"]:
    print(f"- {result['article']['title']} (Score: {result['similarity_score']:.2f})")
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m e2e          # End-to-end tests only
```

### Test Structure

```
tests/
├── unit/               # Fast unit tests
├── integration/        # Integration tests with external services
└── e2e/               # End-to-end API tests
```

## 📊 Monitoring & Observability

### Health Checks

```http
GET /api/v1/health/          # Basic health check
GET /api/v1/health/detailed  # Detailed system health
GET /api/v1/health/ready     # Kubernetes readiness
GET /api/v1/health/live      # Kubernetes liveness
```

### Logging

Structured logging with:
- **Development**: Colored console output
- **Production**: JSON-formatted logs
- **Request tracking**: Unique request IDs
- **Context preservation**: User and request context

### Metrics

When `ENABLE_METRICS=true`:
- Prometheus metrics endpoint: `/metrics`
- Application performance metrics
- Business logic metrics
- Infrastructure health metrics

## 🚢 Deployment

### Docker Production Deployment

```bash
# Build production image
docker build -t news-anchor-rag .

# Run with production config
docker run -d \
  --name news-anchor \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e DATABASE_URL=postgresql://... \
  news-anchor-rag
```

### Kubernetes Deployment

See `k8s/` directory for Kubernetes manifests:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Environment-Specific Considerations

#### Development
- Debug mode enabled
- Colored logging
- Auto-reload on changes
- Relaxed CORS settings

#### Production
- JSON structured logging
- Security headers enabled
- Rate limiting active
- Health check endpoints
- Metrics collection

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Write** tests for your changes
4. **Ensure** tests pass and code is formatted:
   ```bash
   # Format code
   black src tests scripts
   isort src tests scripts
   
   # Run linting
   flake8 src tests scripts
   mypy src
   
   # Run tests
   pytest
   ```
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Code Style

- **Black** for code formatting
- **isort** for import sorting
- **Type hints** for all functions
- **Docstrings** for public APIs
- **Clean Architecture** principles

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** team for the excellent web framework
- **LangChain** team for the LLM application framework  
- **ChromaDB** team for the vector database
- **OpenAI** for the language models
- The open-source community for amazing tools and libraries

## 📞 Support

- **Documentation**: [docs.newsanchor.com](https://docs.newsanchor.com)
- **Issues**: [GitHub Issues](https://github.com/newsanchor/rag-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/newsanchor/rag-system/discussions)
- **Email**: support@newsanchor.com

---

**Made with ❤️ by the News Anchor Team**