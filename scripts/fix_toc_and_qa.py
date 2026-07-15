from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# 1. Fix TOC Balance
toc_heading = soup.find(string=re.compile('สารบัญเนื้อหา'))
if toc_heading:
    parent_row = toc_heading.find_parent('div', class_='row')
    if parent_row:
        # The row contains the columns
        inner_row = parent_row.find('div', id='row-1646761814')
        if inner_row:
            cols = inner_row.find_all('div', class_='col', recursive=False)
            if len(cols) == 2:
                col_left = cols[0]
                col_right = cols[1]
                
                # Delete right column (it contains the old junk)
                col_right.decompose()
                
                # Make left column full width
                col_left['class'] = ['col', 'small-12', 'large-12']
                
                # Add CSS column-count to the UL
                ul = col_left.find('ul')
                if ul:
                    ul['style'] = "column-count: 2; column-gap: 40px;"
                    ul.clear()
                    
                    def add_li(title, target_h2_text):
                        h2 = soup.find('h2', string=re.compile(target_h2_text))
                        anchor_name = ''
                        if h2:
                            span = h2.find_previous_sibling('span', class_='scroll-to')
                            if span:
                                a = span.find('a')
                                if a and a.has_attr('name'):
                                    anchor_name = '#' + a['name']
                        if anchor_name:
                            li = soup.new_tag('li')
                            li['style'] = "break-inside: avoid; margin-bottom: 10px;"
                            a = soup.new_tag('a', href=anchor_name)
                            span_title = soup.new_tag('span')
                            span_title['style'] = "font-weight: 400;"
                            span_title.string = title
                            a.append(span_title)
                            li.append(a)
                            ul.append(li)

                    # Re-add items
                    add_li('ฟิลเลอร์สะโพก คืออะไร', 'ฟิลเลอร์สะโพก คืออะไร')
                    add_li('เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร', 'เลือกฉีดฟิลเลอร์สะโพก ดีกว่าการผ่าตัดเสริมซิลิโคนอย่างไร')
                    add_li('ฉีดฟิลเลอร์สะโพกด้วยยี่ห้อ Variofill', 'ฟิลเลอร์สะโพก Variofill')
                    add_li('เทคนิคและขั้นตอนการฉีดฟิลเลอร์สะโพก', 'เทคนิคการฉีดฟิลเลอร์สะโพก')
                    add_li('ผลลัพธ์อยู่ได้นานแค่ไหน & อาการข้างเคียงที่อาจเกิดขึ้น', 'ผลลัพธ์อยู่ได้นานแค่ไหน')
                    add_li('การปฏิบัติตัวก่อน-หลังการฉีดฟิลเลอร์สะโพก', 'การปฏิบัติตัวก่อน-หลัง')
                    add_li('ฟิลเลอร์สะโพก ราคาเท่าไหร่', 'ราคาเท่าไหร่')
                    add_li('ฉีดฟิลเลอร์สะโพกกับหมอขนม (RWC Clinic) ดีอย่างไร', 'หมอขนม')
                    add_li('รีวิวการฉีดฟิลเลอร์สะโพก', 'รีวิวการฉีดฟิลเลอร์สะโพก')
                    add_li('Q&A คำถามที่พบบ่อย', 'Q&A')


# 2. Swap Q&A and Reviews
content = soup.find('div', class_='content-area')

def get_block(h2_text):
    h2 = soup.find('h2', string=re.compile(h2_text))
    if h2:
        curr = h2
        while curr and curr.parent != content:
            curr = curr.parent
        return curr
    return None

qa_block = get_block('Q&A')
review_block = get_block('รีวิวการฉีดฟิลเลอร์สะโพก')

if qa_block and review_block:
    idx_qa = content.contents.index(qa_block)
    idx_rev = content.contents.index(review_block)
    
    # QA is currently before Reviews. We want QA after Reviews.
    if idx_qa < idx_rev:
        # We need to extract all blocks related to QA.
        # Let's find the next block after QA that has an H2.
        blocks_to_move = []
        for i in range(idx_qa, len(content.contents)):
            block = content.contents[i]
            if block.name:
                # if this block is review_block, stop.
                if block == review_block:
                    break
                blocks_to_move.append(block)
        
        # Extract them
        for b in blocks_to_move:
            b.extract()
            
        # Insert them after the entire Review section
        # The review section has the main block + gallery blocks. 
        # So we find the next section after Review (which is บทสรุป)
        summary_block = get_block('บทสรุป')
        target = summary_block if summary_block else None
        
        if target:
            for b in reversed(blocks_to_move):
                target.insert_before(b)
        else:
            # just append
            for b in blocks_to_move:
                content.append(b)
                
        print("Moved Q&A after Reviews.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
print("Fixed TOC Balance and QA order.")
