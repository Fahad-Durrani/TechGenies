# TechGenies AI Chatbot Documentation

## Table of Contents
1. Project Overview
2. APIs Used
   - 2.1 Weather API
   - 2.2 News API
3. Environment Setup
   - 3.1 Prerequisites
   - 3.2 Step-by-Step Setup
4. Configuration
5. Code Structure & Organization
6. Logging Mechanism
7. Conversational Flow & User Experience
   - 7.1 Natural, Context-Aware Responses
   - 7.2 Context Retention & Follow-Up Handling
   - 7.3 Handling Clarifications & Ambiguity
8. API Integration & Functionality
   - 8.1 Weather API
   - 8.2 News API
9. Troubleshooting & FAQ
10. Appendix: Example Usage
   - 10.1 Getting the Weather
   - 10.2 Getting the News
   - 10.3 Summary of Features

---

# 1. Project Overview
TechGenies is a conversational AI assistant that provides users with up-to-date news and weather information. The bot integrates with external APIs to fetch real-time data and maintains a high-quality conversational experience. All interactions are logged for traceability and debugging.

# 2. APIs Used

## 2.1 Weather API
• Source: https://www.weatherapi.com/
• Purpose: Provides current weather information such as temperature, humidity, wind speed and condition (sunny, rainy) for a given location.
• Endpoint URL: 
   - Weather: "http://api.weatherapi.com/v1/current.json"
• API key:  The API key is securely stored in the .env file.
• Usage: 
This API is used to answer questions like: 
   - What’s the weather in New York?
   - What is weather, humidity and wind speed in London

## 2.2 News API
• Source: https://newsapi.org/
• Purpose: Fetches the latest news headlines and articles based on user queries.
• Endpoint URL: 
   - Top Headlines: "https://newsapi.org/v2/top-headlines"
   - Everything: "https://newsapi.org/v2/everything"
• API key: The API key is securely stored in the .env file.
• Usage: 
These endpoints are used to answer questions like:
   - Show me top headlines.
   - Show me technology news.

# 3. Environment Setup

## 3.1 Prerequisites
• Python Version: 3.13
• Package Manager: uv
• Terminal: PowerShell (recommended for Windows users)
• IDE: Cursor or VS Code (recommended)

## 3.2 Step-by-Step Setup
1. Install uv
   Open your terminal and run command: 
   pip install uv
2. Initialize the Project Workspace
   Navigate to your project directory as:
   cd path\to\TechGenies
   Run command: uv init
3. Create a Virtual Environment
   uv venv
   This creates a .venv folder in your project directory.
4. Activate the Virtual Environment
   Copy this from messages and run in terminal: 
   .venv\Scripts\activate. 
   Your prompt should now show the environment is active.
5. Install Project Requirements
   Ensure requirement.txt is in your project root (in project TechGenies), then run command: 
   uv add -r requirement.txt
6. Set Your API Keys
   Place your OpenAI key in a .env file or as environment variables as required by our codebase.
   Example .env file:
      - OPENAI_API_KEY=your_openai_key
      - NEWS_API_KEY=newsapi_key (Already added)
      - WEATHER_API_KEY=weatherapi_key (Already added)
7. Run the project command:
   python -u main.py
8. Stop the Project
   Type exit or quit in the terminal.

# 4. Configuration
• Store all API keys in a .env file in the project root 
• The codebase uses the python-dotenv package to load environment variables automatically.
• You only need to add your OpenAI API key to the .env file; the News API and Weather API keys are already provided

# 5. Code Structure & Organization
• main.py: Entry point for the application; handles user input and orchestrates responses.
• agent.py: Core logic for the conversational agent.
• api_import.py: Handles API requests and responses.
• utils/log_helper.py: Logging utilities for agent logs (AI message, Human message, tool calls).
• tools/news_tool.py: News API integration logic.
• tools/weather_tool.py: Weather API integration logic.
• log_dir/log_file.log: Log file for all interactions and errors.
• prompts/prompt.txt: Contains system prompts or templates used to guide the conversational agent’s behavior and responses
• requirement.txt: List of all Python dependencies.

Directory Structure Example:
```
TechGenies/
│
├── main.py
├── agent.py
├── api_import.py
├── requirement.txt
├── .env
├── log_dir/
│   └── log_file.log
├── tools/
│   ├── news_tool.py
│   └── weather_tool.py
├── utils/
│   └── log_helper.py
└── prompts/
    └── prompt.txt
```

# 6. Logging Mechanism
• Comprehensive Logging:
All user interactions, API requests, responses, and system events are logged in log_dir/log_file.log.
• What Gets Logged:
   - Timestamps: Every log entry includes a precise timestamp for traceability.
   - User Actions: User messages, session starts, and session ends are recorded.
   - Agent Actions: The bot’s responses, state updates, and memory management events (such as memory resets).
   - API Activity:
      - API requests (including endpoint URLs and parameters).
      - API responses (summarized, not full payloads for privacy and performance).
      - Tool calls and their arguments/results.
   - System Events:
      - Initialization of the chatbot, LLM, and system prompts.
      - Configuration and environment loading.
      - State changes (e.g., number of messages in memory).
   - Errors and Exceptions:
      - Missing or invalid environment variables.
      - API errors or failures.
      - Any unexpected exceptions during processing.

# 7. Conversational Flow & User Experience

## 7.1 Natural, Context-Aware Responses
• The bot interprets user queries for weather and news in natural language, responding in a way that feels conversational and human-like.
• It understands both direct questions “What’s the weather in Paris?” ,”top headlines”, “ Russia Ukraine conflict news” ,”H1- visa”

## 7.2 Context Retention & Follow-Up Handling
The bot is designed to maintain a natural conversational flow by remembering recent messages and supporting follow-up questions. Here’s how context retention and memory management work:
• Short-Term Memory:
The bot maintains the context of the conversation for up to max_history consecutive messages (default: 12). This allows users to ask follow-up questions or refer to previous topics without needing to repeat themselves
Example:
   - User: What’s the weather in London?
   - Bot: Provides the weather for London.
   - User: And in Paris?
   - Bot: Understands the user is still asking about weather and provides the weather for Paris.
• Memory Reset:
After the number of messages exceeds max_history, the bot’s memory resets and only the last keep_n messages (default: 2) are retained for context. This helps manage resources and ensures privacy, but users may need to restate their context if the conversation is long.
Example:
   - If max_history = 12 and keep_n = 2, after the 13th message, only the 12th and 13th messages are used for context.

## 7.3 Handling Clarifications & Ambiguity
If a user’s request is unclear or ambiguous, the bot will politely ask for clarification.

Example:
User: Show me news.
Bot: Would you like news on a specific topic or the latest top headlines?

# 8. API Integration & Functionality

## 8.1 Weather API
• Current Weather Information:
The bot provides real-time weather updates for any specified city or country. Users can explicitly ask for details such as temperature, humidity, and wind speed, and the bot will include these in its response.
• Error Handling:
The system handles errors related to invalid locations, API issues, or missing data, and informs the user accordingly.

## 8.2 News API
• Top Headlines:
When a user requests "top headlines," the bot automatically fetches and displays the latest top news headlines from the USA.
• Custom News Queries:
Users can request news on any topic, and the bot will provide relevant articles based on the query.
   - Date Filtering: Users can specify a date range to filter news results. Note that the API may restrict results to recent or limited date ranges.
   - Source Filtering: Users can request news from specific sources (e.g., BBC, CNN) by mentioning them in their query.
• Error Handling:
The system gracefully manages errors such as invalid API keys, unavailable results, or API limitations, and provides clear feedback to the user.

# 9. Troubleshooting & FAQ
- I get an error about missing API keys. Ensure your .env file is present and contains valid keys.
- The bot doesn’t respond to my queries. Check that your virtual environment is activated and all dependencies are installed.
- Logs are not being written. Ensure the log_dir directory exists and is writable.

# 10. Appendix: Example Usage

## 10.1 Getting the Weather
User: What’s the weather in Tokyo?
Bot:  Provides the current weather conditions for the requested city, such as temperature.
• If the user explicitly asks for additional details (e.g., humidity, wind speed), the bot will include those in the response.
Example:
User: What’s the weather in Tokyo, including humidity and wind speed?
Bot: Provides temperature, humidity, and wind speed for Tokyo.

## 10.2 Getting the News

User: Show me technology news.
Bot: Returns a list of the latest news articles relevant to the requested topic. For each article, the bot provides:
• The headline (as a clickable link)
• The news source
• A brief summary
• The publication date
User: Show me only the headlines for sports news.
Bot: Returns a list of article titles as clickable links, without summaries or additional details.

User: Show me top headlines.
Bot: Returns the latest top news headlines from the USA, regardless of topic or other filters.
User: Show me USA H-1B visa news from BBC
Bot: Returns only BBC articles related to H-1B visa news in the USA, including the headline, source, summary, and publication date.

## 10.3 Summary of Features
- For weather queries, users receive a concise summary of current conditions for any specified location. Additional details like humidity and wind speed are included only if explicitly requested.
- For news queries, users receive a curated list of recent articles, each with key details and direct access to the full story. If only headlines are requested, the response will include just the article titles.
- When a user requests "top headlines," the bot always provides the latest top news headlines from the USA.
- Users can specify particular news sources (such as BBC, CNN) in their query. When a source is mentioned, the bot will only include articles from that source in its response.

