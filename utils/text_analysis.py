import textstat
import re
from typing import Dict, Any

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyze the quality of the text based on readability, clarity, and technical level.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing analysis metrics
    """
    # Initialize the result dictionary
    results = {}
    
    # Calculate readability using Flesch Reading Ease
    # Higher score = easier to read (0-100 scale)
    readability_score = textstat.flesch_reading_ease(text)
    # Ensure the score is within 0-100 range
    readability_score = max(0, min(readability_score, 100))
    results["readability"] = readability_score
    
    # Calculate clarity score (custom metric)
    clarity_score = calculate_clarity_score(text)
    results["clarity"] = clarity_score
    
    # Calculate technical level (based on jargon and complexity)
    technical_level = calculate_technical_level(text)
    results["technical_level"] = technical_level
    
    # Add other useful metrics
    results["sentence_count"] = textstat.sentence_count(text)
    results["word_count"] = textstat.lexicon_count(text)
    results["grade_level"] = textstat.coleman_liau_index(text)
    
    return results

def calculate_clarity_score(text: str) -> float:
    """
    Calculate a clarity score based on sentence length, word complexity, etc.
    
    Args:
        text: The text to analyze
        
    Returns:
        Clarity score between 0-100
    """
    # Average words per sentence (shorter is generally clearer)
    sentence_count = max(1, textstat.sentence_count(text))
    word_count = textstat.lexicon_count(text)
    avg_words_per_sentence = word_count / sentence_count
    
    # Penalize very long sentences
    sentence_length_score = 100 - min(100, max(0, (avg_words_per_sentence - 15) * 5))
    
    # Percentage of complex words (syllables > 2)
    syllable_count = textstat.syllable_count(text)
    avg_syllables_per_word = syllable_count / max(1, word_count)
    syllable_score = 100 - min(100, max(0, (avg_syllables_per_word - 1.5) * 50))
    
    # Check for passive voice (rough estimation)
    passive_voice_count = len(re.findall(r'\b(?:is|are|was|were|be|been|being)\s+\w+ed\b', text, re.IGNORECASE))
    passive_ratio = passive_voice_count / max(1, sentence_count)
    passive_score = 100 - min(100, passive_ratio * 100)
    
    # Overall clarity score (weighted average)
    clarity_score = (sentence_length_score * 0.4) + (syllable_score * 0.4) + (passive_score * 0.2)
    
    return round(clarity_score, 1)

def calculate_technical_level(text: str) -> float:
    """
    Calculate the technical level based on jargon, acronyms, etc.
    
    Args:
        text: The text to analyze
        
    Returns:
        Technical level score between 0-100 (higher = more technical)
    """
    # List of technical terms related to Abnormal Security
    technical_terms = [
        "API", "authentication", "authorization", "bandwidth", "backend", "cache",
        "CDN", "certificate", "client", "cluster", "configuration", "CPU", "daemon",
        "database", "DNS", "endpoint", "environment", "error", "exception", "firewall",
        "frontend", "gateway", "header", "HTTP", "HTTPS", "instance", "JSON", "latency",
        "load balancer", "memory", "microservice", "network", "node", "packet",
        "platform", "protocol", "proxy", "query", "rate limit", "request", "response",
        "REST", "router", "server", "session", "SSL", "storage", "throughput", "timeout",
        "TLS", "token", "traffic", "URL", "virtualization", "VPN", "webhook", "XML",
        "vulnerability", "sandbox", "phishing", "malware", "ransomware", "encryption",
        "decryption", "payload", "exploit", "credential", "authentication"
    ]
    
    # Count technical terms
    technical_term_count = 0
    for term in technical_terms:
        technical_term_count += len(re.findall(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE))
    
    # Count acronyms (uppercase words of 2-5 letters)
    acronym_count = len(re.findall(r'\b[A-Z]{2,5}\b', text))
    
    # Calculate technical score based on term density
    word_count = max(1, textstat.lexicon_count(text))
    technical_term_density = (technical_term_count + acronym_count) / word_count
    technical_score = min(100, technical_term_density * 500)  # Scale to 0-100
    
    return round(technical_score, 1) 