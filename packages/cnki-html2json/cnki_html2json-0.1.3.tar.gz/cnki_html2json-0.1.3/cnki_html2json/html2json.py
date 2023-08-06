# -*- coding: utf-8 -*-
import re
import json
import os
from lxml import html

def _extract_nodes(long_nodes_list:list,short_nodes_list:list):
	"""提取两个节点列表的差集"""
	if short_nodes_list:
		result = []
		for node in long_nodes_list:
			if node not in short_nodes_list:
				result.append(node)
			else:
				return result
	else:
		return long_nodes_list

def _concat_nodes_value(nodes_list,task:str):
	"""合并节点列表的值"""

	if task == 'reference':
		if nodes_list:
			try:
				result = sorted({int(i) for i in [node.text for node in nodes_list if node.text is not None]})
			except ValueError:
				result = sorted({int(i) for i in [eval(node.text)[0] for node in nodes_list if node.text is not None]})
			return result
		else:
			return []
	
	else:
		if nodes_list:
			result = ' '.join([node.text.strip() for node in nodes_list if node.text is not None])
			return result.strip()
		else:
			return ''

def _process_level_2_chapter(level_2_chapter:list):
	"""处理二级章节标题"""
	chapters = []
	unusual_chapters = {}
	for idx, chapter in enumerate(level_2_chapter):
		if re.match(r'^\d{1}[\.．]{1}\d{1}\.?\d?\s*\w+',chapter):
			chapters.append(chapter)
		elif re.match(r'^\d{1}[\.．]{1}\d{1}\.?\d?\s*$',chapter):
			chapters.append(level_2_chapter[idx+1])
			unusual_chapters[chapter] = level_2_chapter[idx+1]
	return chapters, unusual_chapters

def _process_level_1_chapter(level_1_chapter:list):
	"""处理一级章节标题"""
	chapters = []
	unusual_chapters = {}
	other_chapters = []
	for idx, chapter in enumerate(level_1_chapter):
		if re.match(r'^[0-9一二三四五六七八九][\s\.、．]*\D*[\u4e00-\u9fa5]+',chapter):
			chapters.append(chapter)
		elif re.match(r'^[0-9一二三四五六七八九][\s\.、．]*[^\u4e00-\u9fa5]*',chapter):
			chapters.append(level_1_chapter[idx+1])
			unusual_chapters[chapter] = level_1_chapter[idx+1]
		elif re.match('作者贡献声明|利益冲突声明|参考文献|注释',chapter):
			other_chapters.append(chapter)
	
	# 去重
	# chapters_ = []
	# for i in chapters:
	# 	if i not in chapters_:
	# 		chapters_.append(i)
	return chapters, unusual_chapters, other_chapters

class _ExtractContent:
	"""提取文献内容"""

	def __init__(self,resp_content:str,mode:str="structure") -> None:

		"""
		resp_content: html字符串
		mode: structure:提取结构化文本(默认); plain:提取纯文本; raw:原生格式，会在正文中保留参考文献文献的索引
		"""
		self.content = resp_content
		# self.content = resp_content.replace('<!DOCTYPE html>','').strip()
		self.html_general = html.fromstring(self.content)
		
		if mode != "raw":
			self.html_text = html.fromstring(re.sub('<citation.*?</citation>|<sup>.*?</sup>|<i>.*?</i>','',self.content,flags=re.S))
		
		else:
			# 匹配并替换
			pattern = r'<citation.*?>.*?</citation>'
			content_ = self.content

			# 网页请求的源码
			if content_.split('\n',1)[0] == '<!DOCTYPE html>': 
				for match in re.findall(pattern, content_,flags=re.S):
					match_result = '{}'.format([int(i) for i in re.findall(r'<a class="sup">(\d+)</a>',match)])
					content_ = content_.replace(match, match_result)
			
			# 使用driver.page_source获取的源码
			else: 
				for match in re.findall(pattern, content_,flags=re.S):
					match_result = '{}'.format([int(i) for i in re.findall(r'href="javascript:void\(0\);">(\d+)</a>',match,flags=re.S)])
					content_ = content_.replace(match, match_result)
				
			self.html_text = html.fromstring(re.sub(r'<sup>.*?</sup>|<i>.*?</i>','',content_,flags=re.S))

		self.error = False
		# self.annotation = False
		self.no_structure = False
		self.prefix = False
		self.mode = mode
		
		try:
			raw_level_1_chapter:list = self.html_general.xpath('//h3//text()')
			self.main_level_1_chapter,self.unusual_level_1_chapter,self.other_level_1_chapter = _process_level_1_chapter(raw_level_1_chapter)
			self.level_1_chapter = self.main_level_1_chapter+self.other_level_1_chapter
			if self.unusual_level_1_chapter:
				self.unusual_level_1_chapter_reverse = {v:k for k,v in self.unusual_level_1_chapter.items()}
			
		except AttributeError:
			self.error = True
		
		else:
			# 判断是否是正常文章
			if "参考文献" not in self.level_1_chapter:
				self.error = True
			
		if not self.error:
			self.level_1_chapter_num = len(self.level_1_chapter)
			raw_level_2_chapter:list = self.html_general.xpath('//h4//text()')
			self.level_2_chapter,self.unusual_level_2_chapter = _process_level_2_chapter(raw_level_2_chapter)

			self.text = {}
			# 判断是否存在没有章节标题的前言
			if prefix := self.html_text.xpath('//h3[1]/preceding-sibling::div[@class="p1"]/p'):
				prefix_text = _concat_nodes_value(prefix,'text')
				prefix_citaion_index = _concat_nodes_value(
					self.html_general.xpath('//h3[1]/preceding-sibling::div[@class="p1"]/p/reference/sup/a'),'reference')
				self.text = {'0':{'reference':prefix_citaion_index,'text':prefix_text}}
				self.prefix=True

			# 处理没有篇章结构的文章
			if self.level_1_chapter_num==0:
				prefix_ = self.html_text.xpath('//div[@class="brief"][last()]/following-sibling::div[@class="p1"]/p')
				if prefix_:
					prefix_text = _concat_nodes_value(prefix_,'text')
					prefix_citaion_index = _concat_nodes_value(
						self.html_general.xpath('//div[@class="brief"][last()]/following-sibling::div[@class="p1"]/p/reference/sup/a'),'reference')
					self.text = {'0':{'reference':prefix_citaion_index,'text':prefix_text}}
					self.no_structure = True
			
			self.text |= {k:{} for k in self.level_1_chapter if k!='参考文献'}

	def __generate_xpath(self,chapter_name:str,chapter_class:int,task:str,add_b_label = False,add_font_label=False)->str:
		"""生成xpath
		param chapter_name: 章节名称
		param chapter_class: 章节等级，取1或2
		"""

		if add_font_label==True:
			xpath_ = f'//h{chapter_class+2}/font[text()="{chapter_name}"]/../following-sibling::div/p/font'
			if task == 'reference':
				xpath_ += '/citation/sup/a'
			return xpath_
		
		elif add_b_label==True:
			xpath_ = f'//h{chapter_class+2}/b[text()="{chapter_name}"]/../following-sibling::div/p'
			if task == 'reference':
				xpath_ += '/citation/sup/a'
			return xpath_
		
		else:
			xpath_ = f'//h{chapter_class+2}[text()="{chapter_name}"]/following-sibling::div/p'
			if task == 'reference':
				xpath_ += '/citation/sup/a'
			return xpath_
		
	def __obtain_nodes_list(self,chapter_name:str,chapter_class:int,task:str):
		"""获取节点列表，依次尝试三种xpath表达式"""
		
		if task == 'text':
			html = self.html_text
		else:
			html = self.html_general

		xpath_expression = self.__generate_xpath(chapter_name,chapter_class,task)
		if result:= html.xpath(xpath_expression):
			return result
		
		else:
			xpath_expression = self.__generate_xpath(chapter_name,chapter_class,task,add_b_label=True)
			if result:=html.xpath(xpath_expression):
				return result
		
			else:
				xpath_expression = self.__generate_xpath(chapter_name,chapter_class,task,add_font_label=True)
				return html.xpath(xpath_expression)
	
	def extract_plain_text(self):
		"""提取纯文本"""

		if self.no_structure:
			return self.text['0']['text'] # type:ignore
		
		else:
			total_nodes_list = self.__obtain_nodes_list(self.main_level_1_chapter[0],1,'text')
			other_nodes_list = self.__obtain_nodes_list(self.other_level_1_chapter[0],1,'text')
			valid_nodes_list = _extract_nodes(total_nodes_list,other_nodes_list)
			total_text = _concat_nodes_value(valid_nodes_list,'text')
			
			if self.prefix:
				return self.text['0']['text']+' '+total_text # type:ignore
			else:
				return total_text

	def __extract(self,task:str)->None:
		
		if self.error:
			self.text = None
			return None
		
		offset = 1
		# if not self.annotation and "注释" in self.level_1_chapter:
		if "注释" in self.level_1_chapter:
			offset = 2

		end_idx = self.level_1_chapter_num-offset
		if task == 'reference':
			end_idx = self.level_1_chapter_num-len(self.other_level_1_chapter)
		
		idx = 0
		while idx < end_idx:
			first_nodes_list = self.__obtain_nodes_list(self.level_1_chapter[idx],1,task)
			second_nodes_list = self.__obtain_nodes_list(self.level_1_chapter[idx+1],1,task)

			# 筛选出二级章节
			current_node_idx = self.level_1_chapter[idx].strip()[0]
			
			if current_node_idx in list('123456789'):
				current_level_2_chapter_list = [i for i in self.level_2_chapter if i[0]==current_node_idx]
				if self.unusual_level_2_chapter:
					current_level_2_chapter_list += [self.unusual_level_2_chapter[i] for i in self.unusual_level_2_chapter if i[0]==current_node_idx]
			else:
				current_level_2_chapter_list = []
			
			if current_level_2_chapter_list:
				
				text_ = {}
				current_level_2_chapter_num = len(current_level_2_chapter_list)
				idx_ = 0
				while idx_ < current_level_2_chapter_num:
					first_nodes_list_ = self.__obtain_nodes_list(current_level_2_chapter_list[idx_],2,task)
		
					if idx_ == current_level_2_chapter_num-1:
						second_nodes_list_ = second_nodes_list

					else:
						second_nodes_list_ = self.__obtain_nodes_list(current_level_2_chapter_list[idx_+1],2,task)
			
					if idx_ == 0:
						following_node_ = _extract_nodes(first_nodes_list,first_nodes_list_)
						text_[current_node_idx+'.0'] = _concat_nodes_value(following_node_,task)

					current_node_ = _extract_nodes(first_nodes_list_,second_nodes_list_)

					current_level_2_chapter = current_level_2_chapter_list[idx_]
					unusual_level_2_chapter_reverse = {v:k for k,v in self.unusual_level_2_chapter.items()}

					if current_level_2_chapter in unusual_level_2_chapter_reverse:
						text_[unusual_level_2_chapter_reverse[current_level_2_chapter]+current_level_2_chapter] = _concat_nodes_value(current_node_,task)
					else:
						text_[current_level_2_chapter_list[idx_]] = _concat_nodes_value(current_node_,task)

					idx_ += 1
				self.text[self.level_1_chapter[idx]][task] = text_ # type: ignore

			else:
				current_node_ = _extract_nodes(first_nodes_list,second_nodes_list)
				current_level_1_chapter = self.level_1_chapter[idx]

				self.text[current_level_1_chapter][task] = _concat_nodes_value(current_node_,task) # type: ignore
			idx += 1

	def extract_reference_index(self):
		"""提取章节引用的文献索引"""

		self.__extract(task='reference')
		return self.text
	
	def extract_text(self):
		"""提取正文"""
		
		self.__extract(task='text')
		return self.text

	def extract_reference(self):
		"""提取参考文献"""
		reference = [doc.strip() for doc in self.html_general.xpath('//div[@id="a_bibliography"]/p/a/text()') if doc.strip()!='']
		reference_with_index = [f'[{idx}] '+re.sub(r'^[\.]+','',doc).strip() for idx,doc in enumerate(reference,1)]
		return reference_with_index

	def extract_all(self)->dict:
		"""提取全部"""
		if self.error:
			return {'body_text':None,'参考文献':None}
		
		result = {}
		citing_docs = self.extract_reference()
		if self.mode != 'plain':
			self.extract_reference_index()
			self.extract_text()
			result = {'body_text':self.text}
		
		elif self.mode == 'plain':
			result = {'body_text':self.extract_plain_text()}
		
		return {**result,**{'参考文献':citing_docs}}

def __export_json(text,json_path):
	"""导出json文件"""
	folder_path = os.path.dirname(json_path)
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
	with open(json_path,'w',encoding='utf-8') as f:
		json.dump(text,f,ensure_ascii=False,indent=4)

def extract(paper_html:str,mode:str='structure',export_path=None):
	"""将论文的html字符串转换为字典
	paper_html: 论文的html字符串
	mode: 模式，structure|plain|raw，默认为structure
	export_path: 导出json文件的路径，默认为None，如果导出json文件，该参数必须指定
	"""
	result = _ExtractContent(paper_html,mode).extract_all()
	if not export_path:
		return result
	else:
		__export_json(result,export_path)