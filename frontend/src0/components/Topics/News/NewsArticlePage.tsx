import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import "./NewsArticlePage.css";

const NewsArticlePage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const { article } = location.state || {};

  if (!article) {
    return (
      <div className="news-article-container">
        <h1>No Article Found</h1>
        <p>The article could not be loaded. Please try again.</p>
        <button onClick={() => navigate("/")}>Go Back to Home</button>
      </div>
    );
  }

  return (
    <div className="news-article-container">
      <div className="scrollable-text-summary">
        <h1>Generated News Article</h1>
        <div className="news-article-content">
        <ReactMarkdown>{article}</ReactMarkdown>
        </div>
      </div>
      <button className="back-button" onClick={() => navigate("/")}>
        Back to Home
      </button>
    </div>
  );
};

export default NewsArticlePage;
