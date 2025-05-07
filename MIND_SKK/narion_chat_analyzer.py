#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Narion Chat Analyzer

A comprehensive tool for analyzing chat logs using NLP techniques.
Developed by Benjamin Poersch
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime
from collections import Counter, defaultdict

# NLP libraries
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

# For topic modeling
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# For visualization
import matplotlib.pyplot as plt
import seaborn as sns


class NarionChatAnalyzer:
    """Main class for chat log analysis."""

    def __init__(self):
        self.chat_data = []
        self.users = set()
        self.processed_messages = []
        self.download_nltk_resources()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def download_nltk_resources(self):
        """Download necessary NLTK resources."""
        resources = ['punkt', 'stopwords', 'wordnet', 'vader_lexicon']
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
            except LookupError:
                print(f"Downloading {resource}...")
                nltk.download(resource, quiet=True)

    def load_chat_file(self, filepath):
        """Load chat data from a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            print(f"Successfully loaded file: {filepath}")
            return self.parse_chat_content(content)
        except Exception as e:
            print(f"Error loading file: {e}")
            return False

    def parse_chat_content(self, content):
        """Parse the chat content into a structured format.
        
        This is a basic implementation. Modify based on your chat format.
        """
        # We'll assume a simple format: [timestamp] username: message
        pattern = r'\[(.*?)\]\s+(.*?):\s+(.*)'
        matches = re.findall(pattern, content, re.MULTILINE)
        
        if not matches:
            print("No matches found with the current pattern. Check your chat format.")
            return False
        
        self.chat_data = []
        for timestamp_str, username, message in matches:
            try:
                # Try to parse timestamp - format may need adjustment
                timestamp = datetime.strptime(timestamp_str.strip(), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # If timestamp parsing fails, use current time
                timestamp = datetime.now()
            
            self.chat_data.append({
                'timestamp': timestamp,
                'username': username.strip(),
                'message': message.strip()
            })
            self.users.add(username.strip())
        
        print(f"Parsed {len(self.chat_data)} messages from {len(self.users)} users")
        return True

    def preprocess_text(self):
        """Clean and preprocess text data."""
        self.processed_messages = []
        for item in self.chat_data:
            text = item['message']
            # Convert to lowercase
            text = text.lower()
            # Remove special characters
            text = re.sub(r'[^\w\s]', '', text)
            # Tokenize
            tokens = word_tokenize(text)
            # Remove stopwords and lemmatize
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                     if token not in self.stop_words and len(token) > 2]
            
            processed_text = ' '.join(tokens)
            self.processed_messages.append({
                'timestamp': item['timestamp'],
                'username': item['username'],
                'original': item['message'],
                'processed': processed_text,
                'tokens': tokens
            })
            
        print(f"Preprocessed {len(self.processed_messages)} messages")

    def analyze_basic_metrics(self):
        """Calculate basic chat metrics."""
        if not self.chat_data:
            print("No data loaded. Please load chat data first.")
            return {}
        
        # Message count per user
        user_message_counts = Counter(item['username'] for item in self.chat_data)
        
        # Word count per user
        user_word_counts = defaultdict(int)
        for item in self.processed_messages:
            user_word_counts[item['username']] += len(item['tokens'])
        
        # Average message length per user
        user_avg_message_length = {}
        for user in self.users:
            user_messages = [item for item in self.processed_messages if item['username'] == user]
            if user_messages:
                total_words = sum(len(item['tokens']) for item in user_messages)
                user_avg_message_length[user] = total_words / len(user_messages)
            else:
                user_avg_message_length[user] = 0
        
        # Time analysis - messages per day
        date_counts = Counter(item['timestamp'].date() for item in self.chat_data)
        
        # Activity hours analysis
        hour_counts = Counter(item['timestamp'].hour for item in self.chat_data)
        
        metrics = {
            'total_messages': len(self.chat_data),
            'total_users': len(self.users),
            'user_message_counts': dict(user_message_counts),
            'user_word_counts': dict(user_word_counts),
            'user_avg_message_length': user_avg_message_length,
            'date_counts': {str(date): count for date, count in date_counts.items()},
            'hour_counts': dict(hour_counts)
        }
        
        return metrics

    def analyze_sentiment(self):
        """Analyze sentiment in the chat messages."""
        if not self.processed_messages:
            print("No processed data. Please preprocess chat data first.")
            return {}
        
        # Overall sentiment
        overall_sentiment = {'pos': 0, 'neg': 0, 'neu': 0, 'compound': 0}
        count = 0
        
        # User sentiment
        user_sentiment = {user: {'pos': 0, 'neg': 0, 'neu': 0, 'compound': 0, 'count': 0} 
                          for user in self.users}
        
        # Message sentiment
        message_sentiments = []
        
        for item in self.chat_data:
            text = item['message']
            sentiment = self.sentiment_analyzer.polarity_scores(text)
            
            # Update overall sentiment
            overall_sentiment['pos'] += sentiment['pos']
            overall_sentiment['neg'] += sentiment['neg']
            overall_sentiment['neu'] += sentiment['neu']
            overall_sentiment['compound'] += sentiment['compound']
            count += 1
            
            # Update user sentiment
            user = item['username']
            user_sentiment[user]['pos'] += sentiment['pos']
            user_sentiment[user]['neg'] += sentiment['neg']
            user_sentiment[user]['neu'] += sentiment['neu']
            user_sentiment[user]['compound'] += sentiment['compound']
            user_sentiment[user]['count'] += 1
            
            # Add to message sentiments
            message_sentiments.append({
                'timestamp': item['timestamp'],
                'username': user,
                'message': text,
                'sentiment': sentiment
            })
        
        # Calculate averages
        if count > 0:
            overall_sentiment['pos'] /= count
            overall_sentiment['neg'] /= count
            overall_sentiment['neu'] /= count
            overall_sentiment['compound'] /= count
        
        for user in user_sentiment:
            user_count = user_sentiment[user]['count']
            if user_count > 0:
                user_sentiment[user]['pos'] /= user_count
                user_sentiment[user]['neg'] /= user_count
                user_sentiment[user]['neu'] /= user_count
                user_sentiment[user]['compound'] /= user_count
        
        return {
            'overall_sentiment': overall_sentiment,
            'user_sentiment': user_sentiment,
            'message_sentiments': message_sentiments
        }

    def extract_topics(self, num_topics=5, num_words=10):
        """Extract main topics from the chat using LDA."""
        if not self.processed_messages:
            print("No processed data. Please preprocess chat data first.")
            return {}
        
        # Create corpus from processed messages
        corpus = [item['processed'] for item in self.processed_messages if item['processed']]
        
        if not corpus:
            print("No text corpus available after preprocessing.")
            return {}
        
        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer(max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(corpus)
        feature_names = vectorizer.get_feature_names_out()
        
        # LDA for topic modeling
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        lda.fit(tfidf_matrix)
        
        # Extract topics
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[:-num_words-1:-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topics.append({
                'id': topic_idx,
                'words': top_words,
                'weight': float(topic.sum())
            })
        
        # Topic distribution per message
        message_topics = []
        topic_distribution = lda.transform(tfidf_matrix)
        
        for i, item in enumerate(self.processed_messages):
            if i < len(topic_distribution):
                dominant_topic = int(topic_distribution[i].argmax())
                message_topics.append({
                    'message_id': i,
                    'username': item['username'],
                    'message': item['original'],
                    'dominant_topic': dominant_topic,
                    'topic_distribution': topic_distribution[i].tolist()
                })
        
        return {
            'topics': topics,
            'message_topics': message_topics
        }

    def analyze_user_participation(self):
        """Analyze user participation patterns."""
        if not self.chat_data:
            print("No data loaded. Please load chat data first.")
            return {}
        
        # Participation over time
        timeline = defaultdict(lambda: defaultdict(int))
        for item in self.chat_data:
            date = item['timestamp'].date()
            user = item['username']
            timeline[str(date)][user] += 1
        
        # Response patterns (simplified)
        responses = defaultdict(lambda: defaultdict(int))
        for i in range(1, len(self.chat_data)):
            prev_user = self.chat_data[i-1]['username']
            curr_user = self.chat_data[i]['username']
            if prev_user != curr_user:
                responses[prev_user][curr_user] += 1
        
        # Engagement score (basic implementation)
        user_engagement = {}
        for user in self.users:
            # Count messages
            message_count = sum(1 for item in self.chat_data if item['username'] == user)
            
            # Count unique days active
            active_days = set(item['timestamp'].date() for item in self.chat_data 
                            if item['username'] == user)
            
            # Count responses to others
            responses_to_others = sum(responses[user].values())
            
            # Count responses from others
            responses_from_others = sum(responses[other][user] for other in responses 
                                     if other != user)
            
            # Simple engagement score
            engagement_score = (message_count * 0.4 + 
                              len(active_days) * 0.2 + 
                              responses_to_others * 0.2 + 
                              responses_from_others * 0.2)
            
            user_engagement[user] = {
                'message_count': message_count,
                'active_days': len(active_days),
                'responses_to_others': responses_to_others,
                'responses_from_others': responses_from_others,
                'engagement_score': engagement_score
            }
        
        return {
            'timeline': {date: dict(users) for date, users in timeline.items()},
            'response_patterns': {user: dict(targets) for user, targets in responses.items()},
            'user_engagement': user_engagement
        }

    def generate_visualizations(self, output_dir='./output'):
        """Generate visualizations from the analysis results."""
        if not self.chat_data:
            print("No data loaded. Please load chat data first.")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get analysis results
        basic_metrics = self.analyze_basic_metrics()
        sentiment_results = self.analyze_sentiment()
        
        # Set plot style
        plt.style.use('ggplot')
        
        # 1. Message count per user
        plt.figure(figsize=(10, 6))
        users = list(basic_metrics['user_message_counts'].keys())
        counts = list(basic_metrics['user_message_counts'].values())
        sns.barplot(x=users, y=counts)
        plt.title('Messages per User')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'messages_per_user.png'))
        plt.close()
        
        # 2. Activity by hour
        plt.figure(figsize=(10, 6))
        hours = list(basic_metrics['hour_counts'].keys())
        hour_counts = list(basic_metrics['hour_counts'].values())
        sns.barplot(x=hours, y=hour_counts)
        plt.title('Activity by Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Messages')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'activity_by_hour.png'))
        plt.close()
        
        # 3. Sentiment by User
        plt.figure(figsize=(12, 6))
        users = list(sentiment_results['user_sentiment'].keys())
        compound_scores = [sentiment_results['user_sentiment'][user]['compound'] 
                         for user in users]
        
        # Color positive vs negative
        colors = ['green' if score >= 0 else 'red' for score in compound_scores]
        
        plt.bar(users, compound_scores, color=colors)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        plt.title('Sentiment by User (Compound Score)')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Compound Sentiment Score')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'sentiment_by_user.png'))
        plt.close()
        
        # 4. Activity Timeline
        try:
            participation = self.analyze_user_participation()
            timeline = participation['timeline']
            
            # Convert to format for plotting
            dates = sorted(timeline.keys())
            users = sorted(self.users)
            
            data = []
            for date in dates:
                for user in users:
                    count = timeline[date].get(user, 0)
                    if count > 0:  # Only include non-zero entries
                        data.append({'date': date, 'user': user, 'count': count})
            
            # Create DataFrame for easy plotting with seaborn
            import pandas as pd
            df = pd.DataFrame(data)
            
            if not df.empty:
                plt.figure(figsize=(14, 8))
                pivot_table = df.pivot(index='date', columns='user', values='count').fillna(0)
                
                # Plot stacked bar chart
                pivot_table.plot(kind='bar', stacked=True, ax=plt.gca())
                plt.title('User Participation Over Time')
                plt.xlabel('Date')
                plt.ylabel('Number of Messages')
                plt.legend(title='User')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, 'participation_timeline.png'))
                plt.close()
        except Exception as e:
            print(f"Error generating timeline visualization: {e}")
        
        print(f"Visualizations saved to {output_dir}")

    def export_results(self, output_dir='./output'):
        """Export analysis results to JSON files."""
        if not self.chat_data:
            print("No data loaded. Please load chat data first.")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get analysis results
        basic_metrics = self.analyze_basic_metrics()
        sentiment_results = self.analyze_sentiment()
        topic_results = self.extract_topics()
        participation_results = self.analyze_user_participation()
        
        # Prepare results for serialization
        for result in [basic_metrics, sentiment_results, topic_results, participation_results]:
            self._prepare_for_serialization(result)
        
        # Export to JSON files
        with open(os.path.join(output_dir, 'basic_metrics.json'), 'w', encoding='utf-8') as f:
            json.dump(basic_metrics, f, indent=2)
        
        with open(os.path.join(output_dir, 'sentiment_analysis.json'), 'w', encoding='utf-8') as f:
            json.dump(sentiment_results, f, indent=2)
        
        with open(os.path.join(output_dir, 'topic_analysis.json'), 'w', encoding='utf-8') as f:
            json.dump(topic_results, f, indent=2)
        
        with open(os.path.join(output_dir, 'user_participation.json'), 'w', encoding='utf-8') as f:
            json.dump(participation_results, f, indent=2)
        
        # Export full combined results
        full_results = {
            'analysis_timestamp': datetime.now().isoformat(),
            'chat_stats': {
                'total_messages': len(self.chat_data),
                'total_users': len(self.users),
                'date_range': [
                    min(item['timestamp'] for item in self.chat_data).isoformat(),
                    max(item['timestamp'] for item in self.chat_data).isoformat()
                ] if self.chat_data else [None, None]
            },
            'basic_metrics': basic_metrics,
            'sentiment_analysis': sentiment_results,
            'topic_analysis': topic_results,
            'user_participation': participation_results
        }
        
        with open(os.path.join(output_dir, 'full_analysis_results.json'), 'w', encoding='utf-8') as f:
            json.dump(full_results, f, indent=2)
        
        print(f"Analysis results exported to {output_dir}")

    def _prepare_for_serialization(self, obj):
        """Prepare nested dictionaries for JSON serialization."""
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if isinstance(v, datetime):
                    obj[k] = v.isoformat()
                else:
                    self._prepare_for_serialization(v)
        elif isinstance(obj, list):
            for item in obj:
                self._prepare_for_serialization(item)


def main():
    """Main function for command line usage."""
    parser = argparse.ArgumentParser(description="Narion Chat Analyzer - Analyze chat logs with NLP")
    parser.add_argument('--file', '-f', help='Path to chat log file')
    parser.add_argument('--output', '-o', default='./output', help='Output directory for results')
    parser.add_argument('--topics', '-t', type=int, default=5, help='Number of topics to extract')
    
    args = parser.parse_args()
    
    analyzer = NarionChatAnalyzer()
    
    # Interactive mode if no file is provided
    if not args.file:
        print("No file specified. Starting in interactive mode.")
        filepath = input("Enter the path to your chat log file: ")
    else:
        filepath = args.file
    
    # Load and analyze the chat data
    if analyzer.load_chat_file(filepath):
        analyzer.preprocess_text()
        analyzer.generate_visualizations(args.output)
        analyzer.export_results(args.output)
        print("Analysis complete!")
    else:
        print("Analysis failed. Please check the chat file and try again.")


if __name__ == "__main__":
    main()