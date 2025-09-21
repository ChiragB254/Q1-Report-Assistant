# 📚 RAG Document Assistant

A Streamlit web application that provides an intuitive interface for querying documents using a Retrieval-Augmented Generation (RAG) system. Built specifically for analyzing bank financial reports and Q1 results.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 🌟 Features

- **💬 Interactive Chat Interface**: Ask questions about your documents in natural language
- **📄 Document Upload**: Upload and process PDF, Word, and text documents
- **📊 Database Statistics**: View detailed statistics about processed documents
- **🔧 Document Management**: Manage and delete documents from the database
- **🎨 Dark Theme Answers**: Beautiful dark-themed answer display for better readability
- **⚡ Real-time Processing**: Get instant answers from your document corpus

## 🚀 Live Demo

**[Launch Application](https://your-app-name.streamlit.app)** *(Replace with your actual Streamlit URL)*

## 📁 Project Structure

```
Q1-Report-Assistant/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml      # Local secrets (not committed)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🛠️ Local Development

### Prerequisites

- Python 3.8+
- pip package manager
- Access to RAG API endpoint

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Q1-Report-Assistant.git
   cd Q1-Report-Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure secrets**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   API_BASE_URL = "http://4.156.129.231:8000"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:8501`

## ☁️ Deployment on Streamlit Community Cloud

### Quick Deploy

1. **Fork this repository** to your GitHub account

2. **Deploy to Streamlit**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Choose `app.py` as the main file
   - Click "Deploy"

3. **Configure secrets**
   - Go to your app settings
   - Click "Secrets"
   - Add:
     ```toml
     API_BASE_URL = "http://4.156.129.231:8000"
     ```

### Alternative Deployment Options

- **Heroku**: Deploy using the included `Procfile`
- **Docker**: Use the provided `Dockerfile`
- **Azure**: Deploy to Azure Container Instances
- **AWS**: Use AWS ECS or Lambda

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | RAG API endpoint URL | Required |
| `APP_TITLE` | Application title | "RAG Document Assistant" |
| `MAX_FILE_SIZE` | Maximum upload file size (MB) | 50 |

### Streamlit Configuration

Key settings in `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"        # Blue accent color
backgroundColor = "#ffffff"      # White background
secondaryBackgroundColor = "#f0f2f6"  # Light gray
textColor = "#262730"           # Dark gray text
```

## 📖 Usage Guide

### 1. Asking Questions

- Navigate to the **💬 Chat** tab
- Type your question in the text area
- Click **🔍 Search** to get answers
- View detailed sources in the expandable section

**Example Questions:**
- "What were Scotiabank's capital ratios in Q1 2025?"
- "What was the net income for the quarter?"
- "What are the main risk factors mentioned?"

### 2. Uploading Documents

- Go to the **📄 Upload Documents** tab
- Select a file (PDF, Word, Text, Markdown, HTML)
- Choose processing options
- Click **📤 Upload and Process**

### 3. Viewing Statistics

- Check the **📊 Database Stats** tab
- View total chunks, documents, and collection status
- See detailed document information

### 4. Managing Documents

- Use the **🔧 Management** tab
- View all processed documents
- Delete documents if needed
- Refresh statistics

## 🔌 API Integration

This application connects to a RAG API with the following endpoints:

- `GET /health` - Health check
- `POST /query` - Query documents
- `POST /upload` - Upload documents
- `GET /stats` - Get statistics
- `GET /documents` - List documents
- `DELETE /documents/{filename}` - Delete document

### API Request Format

```json
{
  "question": "What were the Q1 results?",
  "top_k": 5,
  "answer_style": "concise"
}
```

### API Response Format

```json
{
  "query": "What were the Q1 results?",
  "answer": "Based on the provided context...",
  "num_sources": 5,
  "processing_info": {
    "query_variations": 5,
    "total_results_before_dedup": 50,
    "unique_results": 31,
    "final_results_after_rerank": 5
  },
  "timestamp": "2025-09-21T03:38:12.469118"
}
```

## 🎨 Features in Detail

### Dark Theme Answer Display

Answers are displayed with a beautiful dark theme featuring:
- Dark gray background for better focus
- Light text for optimal readability
- Blue accent colors for emphasis
- Proper spacing and typography

### Responsive Design

- **Desktop**: Full-width layout with sidebar
- **Tablet**: Collapsed sidebar, responsive columns
- **Mobile**: Single-column layout, touch-friendly buttons

### Error Handling

- **API Connection**: Graceful handling of API downtime
- **Upload Errors**: Clear error messages for failed uploads
- **Timeout Handling**: User-friendly timeout messages
- **CORS Issues**: Helpful troubleshooting information

## 🔒 Security Considerations

- **Secrets Management**: Never commit secrets to the repository
- **API Security**: Ensure your API endpoint is properly secured
- **File Uploads**: File size and type restrictions are enforced
- **CORS Policy**: Configure your API to allow requests from Streamlit domains

## 🐛 Troubleshooting

### Common Issues

**❌ API Connection Failed**
- Check if the API endpoint is accessible
- Verify the `API_BASE_URL` in secrets
- Ensure CORS is properly configured

**❌ File Upload Errors**
- Check file size limits (50MB default)
- Verify supported file formats
- Ensure API upload endpoint is working

**❌ CORS Errors**
- Add Streamlit domain to API CORS settings
- Check network connectivity
- Verify API endpoint URL

### Debug Mode

To enable debug mode locally:
```toml
# .streamlit/config.toml
[global]
developmentMode = true
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include error handling for API calls
- Test on multiple screen sizes
- Update documentation for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/yourusername/rag-document-assistant/issues)
- **Documentation**: Check the [Wiki](https://github.com/yourusername/rag-document-assistant/wiki)
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web framework
- **Hugging Face** - For transformer models and embeddings
- **ChromaDB** - For vector database functionality
- **FastAPI** - For the backend API framework

---

**Made with ❤️ using Streamlit**

*Last updated: September 2025*