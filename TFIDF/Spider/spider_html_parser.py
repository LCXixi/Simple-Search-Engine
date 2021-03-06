from urllib import parse
from bs4 import BeautifulSoup
import re

class HtmlParser(object):
	"""docstring for HtmlParser"""
	def __init__(self):
		super(HtmlParser, self).__init__()

	将得到的URL放入新URL的集合
	def _get_new_urls(self, page_url, soup):
		new_urls = set()

		links = soup.find('div', class_ = "para").find_all('a', href = re.compile(r"/item/*"))
		for link in links:
			new_url = link['href']
			new_full_url = parse.urljoin(page_url, new_url)
			# print(new_full_url)
			new_urls.add(new_full_url)
		return new_urls

	# 根据网格格式，抓取内容
	def _get_new_data(self, page_url, soup):
		res_data = {}

		res_data['url'] = page_url

		title_node = soup.find('dd', class_ = "lemmaWgt-lemmaTitle-title").find('h1')
		res_data['title'] = title_node.get_text()

		summary_node = soup.find('div', class_ = "lemma-summary")
		res_data['summary'] = summary_node.get_text()

		return res_data

	# 用解析器开始解析
	def parse(self, page_url, html_cont):
		if page_url is None or html_cont is None:
			return
		soup = BeautifulSoup(html_cont, 'html.parser', from_encoding = "utf-8")
		new_urls = self._get_new_urls(page_url, soup)
		new_data = self._get_new_data(page_url, soup)

		return new_urls, new_data
