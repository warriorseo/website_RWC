from bs4 import BeautifulSoup

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

content = soup.find('div', class_='content-area')

# 1. Find the promo banner blocks
promo_elements = []
for i in range(2):
    img = content.find('img', src=f'images/hip_filler_{i}.jpg')
    if img:
        curr = img
        while curr and curr.parent != content:
            curr = curr.parent
        if curr and curr not in promo_elements:
            promo_elements.append(curr)

# 2. Extract them from their current location
for el in promo_elements:
    el.extract()

# 3. Create the new Promotion Section
promo_section = soup.new_tag('div')
promo_section['style'] = "margin-top: 40px; margin-bottom: 40px;"

heading_row = BeautifulSoup('''
<div class="row">
    <div class="col small-12 large-12">
        <h2 style="color: #154a5c; text-align: center;">โปรโมชั่นฟิลเลอร์สะโพก</h2>
    </div>
</div>
''', 'html.parser')

promo_section.append(heading_row)

for el in promo_elements:
    promo_section.append(el)

# 4. Insert it at the bottom (just before the last footer div, or at the very end if footer div isn't obvious)
# The last element is a text-align center footer string. Let's put it before that.
children = [c for c in content.contents if c.name]
last_child = children[-1] if children else None

if last_child and 'padding:14px 20px' in str(last_child):
    last_child.insert_before(promo_section)
else:
    content.append(promo_section)

print("Created Promotion section and moved banners to the bottom.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(soup.prettify())
