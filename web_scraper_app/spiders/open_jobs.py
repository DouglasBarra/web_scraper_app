import scrapy

class OpenJobsSpider(scrapy.Spider):
    name = "open_jobs"
    start_urls = [""]
    keyword = ""
    seen_links = set()
    visited_pages = set()

    def parse(self, response):
        self.visited_pages.add(response.url)
        self.logger.info(f"Crawling: {response.url}")

        links = response.css('a')

        for link in links:
            href = link.attrib.get("href", "").strip()

            if not href or any(href.startswith(scheme) for scheme in ["mailto:", "tel:", "javascript:", "#"]):
                continue

            full_url = response.urljoin(href)

            if self.keyword.lower() in response.text.lower():
                self.logger.info(f"✅ Matched: {response.url}")
                # Optionally, save matched page:
                self.save_url_to_txt(response.url, "Matched Page")
                    

            if (
                (href.startswith('/') or self.allowed_domain_link(full_url)) and
                full_url not in self.visited_pages
            ):
                self.visited_pages.add(full_url)
                yield scrapy.Request(full_url, callback=self.parse)

    def save_url_to_txt(self, url, link_text):
        if url in self.seen_links:
            return
        self.seen_links.add(url)
        self.logger.info(f"📝 Saving to file: {url} [{link_text}]")
        with open("matched_urls.txt", "a", encoding="utf-8") as f:
            f.write(f"{link_text} -> {url}\n")

    def allowed_domain_link(self, url):
        return "velozient.com" in url