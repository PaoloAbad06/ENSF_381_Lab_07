import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

url = "https://en.wikipedia.org/wiki/University_of_Calgary"

headers = {
    "User-Agent": "lab07-web-analyzer"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Successfully fetched content from {url}")

    # 3. == DATA ANALYSIS ==

    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    heading_count = len(headings)

    links = soup.find_all(['a'])
    link_count = len(links)

    paragraphs = soup.find_all(['p'])
    paragraph_count = len(paragraphs)

    print(f"\nNumber of Headings: {heading_count}")
    print(f"Number of Links: {link_count}")
    print(f"Number of Paragraphs: {paragraph_count}")

    # 4. == WORD FREQUENCY ANALYSIS ==

    text = soup.get_text()
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    word_items = list(word_counts.items())
    
    for i in range(len(word_items)):
        for j in range(i + 1, len(word_items)):
            if word_items[i][1] < word_items[j][1]:
                word_items[i], word_items[j] = word_items[j], word_items[i]

    print("\nTop 5 most frequently occurring words: ")
    for i, (word, count) in enumerate(word_items[:5], 1):
        print(f"{i}. '{word}', count = {count}")

    # 5 == KEYWORD SEARCH ==

    keyword = input("Search Keyword: ")

    keyword_lower = keyword.lower()
    keyword_count = text_lower.count(keyword_lower)

    print(f"\nKeyword: '{keyword}', count = {keyword_count}")

    # 6 == FINDING THE LONGEST PARAGRAPH ==

    paragraphs = soup.find_all('p')

    valid_paragraphs = []
    for i, p in enumerate(paragraphs, 1):
        paragraph_text = p.get_text(strip=True)
        if paragraph_text:
            words = re.findall(r'\b\w+\b', paragraph_text)
            word_count = len(words)
            if word_count >= 5:
                valid_paragraphs.append({
                    'index': i,
                    'text': paragraph_text,
                    'word_count': word_count
                })
    if valid_paragraphs:
        longest = max(valid_paragraphs, key=lambda x: x['word_count'])

        print(f"\nLongest Paragraph: ")
        print(longest['text'])
        print(f"\nLongest Paragraph Word Count = {longest['word_count']} words")

    # 7 == VISUALIZING RESULTS ==

    labels = ['Headings', 'Links', 'Paragraphs']
    values = [heading_count, link_count, paragraph_count]
    plt.bar(labels, values)
    plt.title('Put your Group# Here')
    plt.ylabel('Count')
    plt.xlabel('HTML Element')
    #plt.savefig('web_analysis_results.png') # Save the figure as an image file
    plt.show()


    ##print(soup.prettify())
except Exception as e:
    print(f"Error fetching content: {e}")

