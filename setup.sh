mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor=\"#72de6f\"\n\
backgroundColor=\"#3f3d56\"\n\
secondaryBackgroundColor=\"#3f3d56\"\n\
textColor=\"#ffffff\"\n\
font=\"sans serif\"\n\
" > ~/.streamlit/config.toml