import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urljoin, urlparse

class WebScraper:
    def __init__(self, base_url, max_depth):
        self.base_url = base_url
        self.visited = set()
        self.graph = nx.DiGraph()
        self.max_depth = max_depth

    def crawl(self, url, depth=0):
        if url in self.visited or depth > self.max_depth:
            return
        self.visited.add(url)
        print(f"Crawling: {url}")
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                return
        except requests.RequestException:
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if self.is_valid_url(full_url):
                self.graph.add_edge(url, full_url)
                self.crawl(full_url, depth + 1)

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.scheme in ['http', 'https'] and parsed.netloc == urlparse(self.base_url).netloc

    def plot_graph(self):
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=50, font_size=8, arrows=True)
        plt.title(f"Web Graph for {self.base_url}")
        plt.tight_layout()
        plt.show(block=True)

if __name__ == "__main__":
    base_url = input("Enter the base URL to crawl: ")
    max_depth = int(input("Enter the maximum crawl depth: "))
    scraper = WebScraper(base_url, max_depth)
    scraper.crawl(base_url)
    scraper.plot_graph()
