# Dream AI Interpreter 🌙✨

**AI-Powered Dream Analysis, Visualization & Speech-to-Text Service**

A sophisticated FastAPI-based web service that combines the power of **OpenAI's GPT-3.5 Turbo**, **DALL-E 3**, and **Whisper** to provide comprehensive dream interpretation, visual representation, and voice transcription capabilities. Built with modern Python architecture, this service offers empathetic dream analysis through "Dr. Elena Nightingale," a virtual dream analyst with expertise in Jungian psychology, plus the ability to transcribe spoken dreams into text.

## � Core Features

### 🧠 **Intelligent Dream Analysis**
- **Expert Persona**: Dr. Elena Nightingale - a compassionate dream analyst with 20+ years of experience
- **Jungian Psychology**: Deep symbolic interpretation using established psychological frameworks
- **Emotional Intelligence**: Empathetic responses that acknowledge the dreamer's feelings
- **Comprehensive Output**: Detailed analysis including symbols, emotions, and practical guidance

### 🎨 **Advanced Image Generation**
- **DALL-E 3 Integration**: High-quality, realistic dream visualizations
- **Smart Content Filtering**: Automatic handling of sensitive content with metaphorical representations
- **Contextual Prompting**: AI-generated prompts that capture dream essence while staying policy-compliant
- **Realistic Style**: Focused on photorealistic representations with cinematic lighting

### 🎙️ **Speech-to-Text Transcription**
- **OpenAI Whisper Integration**: State-of-the-art audio transcription
- **Multiple Format Support**: mp3, wav, m4a, mp4, mpeg, mpga, webm
- **Language Detection**: Auto-detect or specify language (25+ languages supported)
- **Large File Support**: Up to 25MB audio files
- **Voice-to-Dream Workflow**: Speak your dreams and get full analysis

### 📊 **Dream Pattern Classification**
- **Six Categories**: Adventure, Nature, Home & Family, Nightmare, Romantic, Fantasy & Surreal
- **Percentage Breakdown**: Quantitative analysis of dream themes
- **Pattern Recognition**: AI-powered categorization based on dream content

### 🏗️ **Production-Ready Architecture**
- **FastAPI Framework**: High-performance, auto-documented REST API
- **Docker Support**: Full containerization with Docker Compose
- **Health Monitoring**: Built-in health checks and status endpoints
- **Scalable Design**: Modular architecture with separation of concerns

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** (recommended) or Python 3.8+
- **OpenAI API Key** with access to GPT-3.5 Turbo and DALL-E 3

### 🐳 Docker Installation (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/SayedLabib/AI_Dream_Interpreter.git
   cd AI_Dream_Interpreter
   ```

2. **Configure environment**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

3. **Launch the service**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - **API Base**: http://localhost:8063
   - **Interactive Docs**: http://localhost:8063/docs
   - **Health Check**: http://localhost:8063/health

### 💻 Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

3. **Run the application**
   ```bash
   python -m app.main
   ```

## 📁 Project Architecture

```
AI_Dream_Interpreter/
├── app/                                    # Main application package
│   ├── main.py                            # FastAPI app & CORS configuration
│   ├── core/                              # Core configuration
│   │   ├── config.py                      # Settings management with Pydantic
│   └── services/                          # Business logic layer
│       └── dream_ai/                      # Dream AI service domain
│           ├── api_manager/               # External API integrations
│           │   ├── image_gen_manager.py   # OpenAI DALL-E & GPT integration
│           │   └── Speech_to_text_manager.py # OpenAI Whisper integration
│           ├── image_gen_service/         # Dream analysis service layer
│           │   ├── image_gen_router.py    # Dream analysis FastAPI routes
│           │   ├── image_gen_schema.py    # Dream analysis Pydantic models
│           │   └── image_gen_service.py   # Dream analysis business logic
│           └── Speech_to_text/            # Speech-to-Text service layer
│               ├── speech_to_text_router.py # STT FastAPI routes
│               └── speech_text_shcema.py  # STT Pydantic models
├── nginx/                                 # Nginx reverse proxy config
│   └── nginx.conf                         # Production-ready proxy settings
├── docker-compose.yml                     # Multi-service orchestration
├── Dockerfile                             # Container definition
├── requirements.txt                       # Python dependencies
├── .env                                   # Environment configuration
├── .gitignore                             # Git ignore rules
└── .dockerignore                          # Docker ignore rules
```

## 🛠️ API Reference

### Dream Analysis Endpoints

#### **POST** `/api/v1/dream-ai/complete-interpretation`
Complete dream analysis with image generation.

**Request Body:**
```json
{
  "dream_description": "I was flying over golden fields with mountains in the distance..."
}
```

**Response:**
```json
{
  "title": "A Journey of Freedom and Aspiration",
  "content": "This beautiful dream of flight represents...",
  "imageUrl": "https://oaidalleapiprodscus.blob.core.windows.net/...",
  "dreamPatterns": {
    "adventure": 75,
    "nature": 60,
    "homeFamily": 10,
    "nightmare": 0,
    "romantic": 5,
    "fantasySurreal": 80
  }
}
```

### Speech-to-Text Endpoints

#### **POST** `/api/v1/speech-to-text/transcribe`
Transcribe audio file to text using OpenAI Whisper.

**Request:**
- **Form Data**: `audio_file` (file, max 25MB)
- **Optional**: `language` (string, e.g., "en", "es", "fr")

**Supported Formats:** mp3, wav, m4a, mp4, mpeg, mpga, webm

**Response:**
```json
{
  "text": "I had this amazing dream where I was flying...",
  "language": "en",
  "filename": "dream_recording.wav",
  "file_size_bytes": 1048576,
  "processing_time": 3.45
}
```

#### **GET** `/api/v1/speech-to-text/supported-formats`
Get information about supported audio formats and limitations.

#### **GET** `/api/v1/speech-to-text/health`
Speech-to-Text service health check.

### Utility Endpoints

- **GET** `/` - API information and model details
- **GET** `/health` - Application health status
- **GET** `/api/v1/dream-ai/health` - Dream analysis service health check
- **GET** `/api/v1/dream-ai/models` - AI model information
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative API documentation

## 🎙️ Using Speech-to-Text

### Basic Audio Transcription
```bash
curl -X POST "http://localhost:8020/api/v1/speech-to-text/transcribe" \
  -F "audio_file=@dream_recording.wav" \
  -F "language=en"
```

### PowerShell Example
```powershell
$form = @{
    audio_file = Get-Item "dream_recording.wav"
    language = "en"
}
Invoke-RestMethod -Uri "http://localhost:8020/api/v1/speech-to-text/transcribe" -Method Post -Form $form
```

### Complete Voice-to-Dream Workflow
1. **Record** your dream description as an audio file
2. **Upload** to `/api/v1/speech-to-text/transcribe` to get text
3. **Use** the transcribed text with `/api/v1/dream-ai/complete-interpretation`
4. **Receive** complete dream analysis with visualization

## 🐳 Docker Deployment Options

The application supports multiple deployment configurations using Docker Compose profiles:

### **Basic Deployment** (FastAPI only)
```bash
docker-compose up --build
```

### **With Nginx Reverse Proxy**
```bash
docker-compose --profile nginx up --build
```

### **With Redis Caching**
```bash
docker-compose --profile redis up --build
```

### **Full Production Stack**
```bash
docker-compose --profile nginx --profile redis up --build
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key with GPT-3.5 & DALL-E access | - | ✅ |
| `APP_NAME` | Application display name | "Dream AI Interpreter" | ❌ |
| `DEBUG` | Enable debug mode | `false` | ❌ |

### Dream Pattern Categories

The AI categorizes dreams into six core patterns with percentage scoring:

- **🏔️ Adventure** - Travel, exploration, journeys, movement, discovery
- **🌿 Nature** - Animals, plants, weather, landscapes, natural elements  
- **🏠 Home & Family** - Houses, family members, childhood, domestic settings
- **😰 Nightmare** - Fear, anxiety, chasing, falling, scary elements
- **💕 Romantic** - Love, intimate moments, passion, relationships
- **✨ Fantasy & Surreal** - Magic, flying, impossible scenarios, transformation

## 🧪 Development & Testing

### Local Development Setup

1. **Virtual Environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   # Create .env file
   OPENAI_API_KEY=your_api_key_here
   DEBUG=true
   ```

3. **Run Development Server**
   ```bash
   python -m app.main
   # or
   uvicorn app.main:app --reload --port 8020
   ```

### Testing the API

Use the included test script:
```bash
python test_endpoint.py
```

Or test manually with curl:
```bash
curl -X POST "http://localhost:8020/api/v1/dream-ai/complete-interpretation" \
     -H "Content-Type: application/json" \
     -d '{"dream_description": "I was flying over beautiful landscapes"}'
```

### Code Quality Standards

- **Type Hints**: All functions use Python type annotations
- **Pydantic Models**: Strict data validation and serialization
- **Error Handling**: Comprehensive exception handling with meaningful messages
- **Logging**: Structured logging for debugging and monitoring
- **Documentation**: Inline docstrings and API documentation

## 📦 Dependencies & Tech Stack

### Core Framework
- **FastAPI 0.104.1** - Modern, fast web framework
- **Uvicorn 0.24.0** - Lightning-fast ASGI server
- **Pydantic 2.5.0** - Data validation using Python type annotations

### AI Integration
- **OpenAI 1.35.0** - Official OpenAI Python client
  - GPT-3.5 Turbo for dream analysis
  - DALL-E 3 for image generation

### Utilities
- **python-dotenv 1.0.0** - Environment variable management
- **httpx 0.25.2** - Async HTTP client for external APIs
- **python-multipart 0.0.6** - Form data parsing

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy and load balancing
- **Redis** - Optional caching layer

## 🚀 Production Deployment

### Performance Optimization
- **Async Operations**: All AI API calls are asynchronous
- **Connection Pooling**: Efficient HTTP connection management
- **Error Recovery**: Graceful handling of API failures
- **Timeout Management**: Proper timeout configurations

### Security Best Practices
- **Environment Variables**: All secrets stored securely
- **CORS Configuration**: Configurable cross-origin settings
- **Input Validation**: Pydantic models prevent injection attacks
- **API Rate Limiting**: Built-in OpenAI rate limit handling

### Monitoring & Health Checks
- **Health Endpoints**: `/health` and service-specific checks
- **Docker Health Checks**: Container-level monitoring
- **Structured Logging**: JSON-formatted logs for easy parsing
- **Error Tracking**: Comprehensive exception logging

### Scaling Considerations
- **Stateless Design**: No server-side session management
- **Horizontal Scaling**: Multiple container instances supported
- **Load Balancing**: Nginx configuration included
- **Caching Strategy**: Optional Redis integration for response caching

## 🔧 Advanced Configuration

### Nginx Customization
Edit `nginx/nginx.conf` for:
- SSL/TLS termination
- Custom routing rules
- Static file serving
- Additional security headers

### Docker Customization
- **Resource Limits**: Configure in `docker-compose.yml`
- **Environment Overrides**: Use Docker Compose environment files
- **Volume Mounts**: Add persistent storage if needed

## 🤝 Contributing

### Development Workflow
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards
- Follow **PEP 8** Python style guidelines
- Include **type hints** for all function parameters and returns
- Write **docstrings** for all public functions and classes
- Add **tests** for new functionality
- Update **documentation** for API changes

## 📊 AI Model Information

### Current Models
- **Chat Model**: `gpt-3.5-turbo`
  - Purpose: Dream analysis and interpretation
  - Context: Jungian psychology and symbolic analysis
  - Persona: Dr. Elena Nightingale

- **Image Model**: `dall-e-3`  
  - Purpose: Dream visualization
  - Style: Realistic with cinematic lighting
  - Safety: Automatic content filtering and metaphorical representations

- **Speech Model**: `whisper-1`
  - Purpose: Audio transcription and speech-to-text
  - Languages: 25+ languages supported with auto-detection
  - Formats: mp3, wav, m4a, mp4, mpeg, mpga, webm

### Model Performance
- **Analysis Time**: ~5-10 seconds per interpretation
- **Image Generation**: ~10-15 seconds per image
- **Audio Transcription**: ~3-8 seconds per minute of audio
- **Total Processing**: ~15-30 seconds end-to-end
- **Rate Limits**: Handled automatically with retry logic

## � Privacy & Security

### Data Handling
- **No Storage**: Dream descriptions are not stored permanently
- **Temporary Processing**: Data exists only during request lifecycle
- **OpenAI Privacy**: Subject to OpenAI's data usage policies
- **HTTPS Ready**: SSL/TLS configuration supported

### API Security
- **Input Validation**: All inputs validated with Pydantic
- **Rate Limiting**: OpenAI rate limits respected
- **Error Sanitization**: No sensitive data in error responses
- **CORS Protection**: Configurable origin restrictions

## 📞 Support & Resources

### Documentation
- **API Docs**: Available at `/docs` when running
- **Code Documentation**: Inline docstrings throughout codebase
- **Architecture Guide**: See project structure section above

### Getting Help
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check `/docs` endpoint for latest API specs

### Community
- **Contributions**: Welcome! See contributing guidelines above
- **Feature Requests**: Submit via GitHub Issues with enhancement label
- **Bug Reports**: Include reproduction steps and environment details

## 📈 Version History & Roadmap

### Current Version: v1.0.0
**Features:**
- ✅ Complete dream interpretation with GPT-3.5 Turbo
- ✅ Realistic image generation with DALL-E 3
- ✅ Speech-to-text transcription with Whisper
- ✅ Six-category dream pattern analysis
- ✅ Dr. Elena Nightingale persona
- ✅ Multi-format audio support (mp3, wav, m4a, etc.)
- ✅ Multi-language transcription (25+ languages)
- ✅ Docker deployment support
- ✅ Comprehensive API documentation
- ✅ Production-ready architecture

### Future Enhancements
- 🔄 **Response Caching** - Redis-based caching for improved performance
- 🔄 **Voice-to-Dream Pipeline** - Direct audio upload to complete dream analysis
- 🔄 **Real-time Transcription** - WebSocket-based live audio processing
- 🔄 **User Accounts** - Optional user authentication and dream history
- 🔄 **Batch Processing** - Multiple dream analysis in single request
- 🔄 **Advanced Analytics** - Dream pattern trends and insights
- 🔄 **Multiple Languages** - International dream analysis support
- 🔄 **Custom Personas** - Alternative analyst personalities

---

**Built with ❤️ for dreamers and developers**

*"Dreams are the royal road to the unconscious" - Sigmund Freud*
