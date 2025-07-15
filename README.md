# Dream AI - AI-Powered Dream Interpretation and Visualization

A FastAPI-based web service that provides AI-powered dream interpretation and visualization using OpenAI's **GPT-3.5 Turbo** for analysis and **DALL-E 3** for image generation.

## 🌟 Features

- **Dream Analysis**: Comprehensive interpretation using **GPT-3.5 Turbo**
- **Dream Visualization**: Generate images with **DALL-E 3**
- **Multiple Styles**: Realistic, artistic, surreal, minimalist, and dark themes
- **RESTful API**: Clean, documented endpoints
- **Docker Support**: Easy deployment with Docker Compose
- **Health Checks**: Built-in monitoring endpoints
- **Model Information**: Endpoint to check which AI models are being used

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_Dream_Interpreter
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the API**
   - API: http://localhost:8020
   - Documentation: http://localhost:8020/docs
   - Health Check: http://localhost:8020/health

## 📁 Project Structure

```
AI_Dream_Interpreter/
├── app/                                 # Main application package
│   ├── core/                           # Core configuration
│   │   ├── __init__.py
│   │   └── config.py                   # Settings and configuration
│   ├── services/                       # Business logic services
│   │   └── dream_ai/                   # Dream AI service package
│   │       ├── api_manager/            # External API management
│   │       │   ├── __init__.py
│   │       │   └── image_gen_manager.py # OpenAI API integration
│   │       └── image_gen_service/      # Main service logic
│   │           ├── __init__.py
│   │           ├── image_gen_router.py  # FastAPI routes
│   │           ├── image_gen_schema.py  # Pydantic models
│   │           └── image_gen_service.py # Business logic
│   ├── __init__.py
│   └── main.py                         # FastAPI application entry point
├── nginx/                              # Nginx configuration (optional)
│   └── nginx.conf
├── .dockerignore                       # Docker ignore rules
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
├── docker-compose.yml                  # Docker Compose configuration
├── Dockerfile                          # Docker image definition
├── README.md                           # This file
├── README-Docker.md                    # Docker-specific documentation
└── requirements.txt                    # Python dependencies
```

## 🛠️ API Endpoints

### Dream Analysis
- **POST** `/api/v1/dream-ai/analyze`
  - Analyze a dream description
  - Returns interpretation, symbolism, emotions, and suggestions

### Image Generation
- **POST** `/api/v1/dream-ai/generate-image`
  - Generate an image based on dream description
  - Supports multiple artistic styles

### Complete Interpretation
- **POST** `/api/v1/dream-ai/complete-interpretation`
  - Full service: analysis + image generation
  - Returns both interpretation and generated image

### Health & Info
- **GET** `/health` - Application health check
- **GET** `/` - API information and model details
- **GET** `/docs` - Interactive API documentation
- **GET** `/api/v1/dream-ai/models` - Information about AI models being used

## 🐳 Docker Configuration

### Single Service (FastAPI only)
```bash
docker-compose up
```

### With Nginx Reverse Proxy
```bash
docker-compose --profile nginx up
```

### With Redis Caching
```bash
docker-compose --profile redis up
```

### Full Stack
```bash
docker-compose --profile nginx --profile redis up
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `APP_NAME` | Application name | "Dream AI Interpreter" |
| `DEBUG` | Debug mode | `false` |

### Supported Image Styles

- `realistic` - Photorealistic with cinematic lighting
- `artistic` - Painterly and expressive style
- `surreal` - Dreamlike and fantastical (Dali-inspired)
- `minimalist` - Clean and simple composition
- `dark` - Moody atmosphere with mysterious lighting

## 🧪 Development

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables in `.env`
3. Run: `python -m app.main`

### Code Style
- Follow PEP 8
- Use type hints
- Document all functions and classes
- Keep functions focused and small

## 📦 Dependencies

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **OpenAI 1.35.0** - AI services integration (GPT-3.5 Turbo + DALL-E 3)
- **Pydantic** - Data validation
- **Python-dotenv** - Environment management

## 🚀 Deployment

### Production Deployment
1. Set production environment variables
2. Use a proper ASGI server (Uvicorn/Gunicorn)
3. Configure reverse proxy (Nginx)
4. Set up SSL certificates
5. Configure monitoring and logging

### Health Monitoring
- Health check endpoint: `/health`
- Docker health checks included
- Monitor OpenAI API usage and limits

## 🔒 Security

- Environment variables for secrets
- CORS configuration
- Input validation with Pydantic
- No sensitive data in logs
- Docker security best practices


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the documentation
- Review existing issues
- Create a new issue with detailed description

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
  - Dream analysis with GPT-4
  - Image generation with DALL-E 3
  - Docker support
  - API documentation
