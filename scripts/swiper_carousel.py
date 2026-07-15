from bs4 import BeautifulSoup
import re

filepath = 'd:/AI-Cyborg-2558/_SEO_Clients/RWC/web/hip_filler_injection.html'
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

wrapper = soup.find('div', class_='steps-carousel-wrapper')

if wrapper:
    # Extract the step data from the current slides
    steps = []
    # Currently they are inside <div class="col small-12 large-12" style="padding: 0 15px;">
    # containing <div class="row align-middle"...> ...
    
    slides = wrapper.find_all('div', class_='align-middle')
    for slide in slides:
        img_container = slide.find('div', style=lambda s: s and 'background-color: #fcfcfc' in s)
        img = img_container.find('img') if img_container else None
        if img: img.extract()
        
        text_container = slide.find('h3').parent if slide.find('h3') else None
        title = slide.find('h3').get_text(strip=True) if slide.find('h3') else 'ขั้นตอน'
        p = slide.find('p')
        text = str(p.decode_contents()) if p else ''
        
        steps.append({'img': img, 'title': title, 'text': text})

    if steps:
        # Create a SwiperJS carousel HTML
        carousel_html = """
        <div class="custom-swiper-wrapper" style="width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw; background-color: #f0f7f6; padding: 60px 0; margin-bottom: 40px; margin-top: 20px; overflow: hidden;">
            <!-- Swiper CSS -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.css" />
            
            <div class="row">
                <div class="col small-12 large-12" style="text-align: center;">
                    <div class="swiper mySwiper" style="width: 100%; padding-bottom: 50px; padding-top: 20px;">
                        <div class="swiper-wrapper">
        """
        
        for step in steps:
            img_html = str(step['img']).replace('style="', 'style="max-width: 100%; height: auto; border-radius: 8px; ') if step['img'] else '<div style="background:#ddd; width:100%; height:250px; display:flex; align-items:center; justify-content:center; color:#999; border-radius:12px;">[No Image]</div>'
            carousel_html += f"""
                            <div class="swiper-slide" style="background-position: center; background-size: cover; width: 80%; max-width: 800px; background-color: #fff; border-radius: 16px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); display: flex; overflow: hidden; flex-direction: row; align-items: center;">
                                <div style="flex: 1; padding: 0; background-color: #fcfcfc; display: flex; align-items: center; justify-content: center;">
                                    {img_html}
                                </div>
                                <div style="flex: 1; padding: 40px; text-align: left;">
                                    <h3 style="color: #476661; font-size: 1.8em; margin-bottom: 15px; font-weight: bold;">{step['title']}</h3>
                                    <p style="color: #666; font-size: 1.05em; line-height: 1.6;">{step['text']}</p>
                                </div>
                            </div>
            """
            
        carousel_html += """
                        </div>
                        <div class="swiper-pagination"></div>
                        <div class="swiper-button-next" style="color: #476661;"></div>
                        <div class="swiper-button-prev" style="color: #476661;"></div>
                    </div>
                </div>
            </div>
            
            <!-- Swiper JS -->
            <script src="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.js"></script>
            <script>
                document.addEventListener('DOMContentLoaded', function () {
                    var swiper = new Swiper(".mySwiper", {
                        effect: "coverflow",
                        grabCursor: true,
                        centeredSlides: true,
                        slidesPerView: "auto",
                        coverflowEffect: {
                            rotate: 0,
                            stretch: 100,
                            depth: 200,
                            modifier: 1,
                            slideShadows: false,
                        },
                        pagination: {
                            el: ".swiper-pagination",
                            clickable: true,
                        },
                        navigation: {
                            nextEl: ".swiper-button-next",
                            prevEl: ".swiper-button-prev",
                        },
                        loop: true,
                        autoplay: {
                            delay: 4000,
                            disableOnInteraction: false,
                        }
                    });
                });
            </script>
            <style>
                @media (max-width: 768px) {
                    .swiper-slide {
                        flex-direction: column !important;
                        width: 90% !important;
                    }
                    .swiper-slide > div {
                        width: 100% !important;
                        flex: none !important;
                    }
                }
            </style>
        </div>
        """
        
        new_soup = BeautifulSoup(carousel_html, 'html.parser')
        wrapper.replace_with(new_soup)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('Successfully replaced Flatsome slider with generic SwiperJS carousel.')
    else:
        print('Could not extract steps data from existing wrapper.')
else:
    print('Wrapper not found.')
