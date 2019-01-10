from seleniumrequests import Firefox
from itertools import combinations
from time import sleep

#%%
def translate_color(s):
    if s == 'rgb(239, 62, 66)':
        return 'red'
    elif s == 'rgb(0, 178, 89)':
        return 'green'
    elif s == 'rgb(73, 47, 146)':
        return 'purple'


def translate_pattern(s):
    if s[0:3] == 'rgb':
        return 'fill'
    elif s[0:3] == 'url':
        return 'striped'
    else:
        return 'empty'


def translate_shape(s):
    return s[1:s.find('-')]


#%%
def organize_cards(page):
    card_array = []

    for card in page:
        card_elements = card.find_elements_by_css_selector('svg')

        number = len(card_elements)

        color = card_elements[0].find_element_by_css_selector('use').get_attribute('stroke')
        color = translate_color(color)

        pattern = card_elements[0].find_element_by_css_selector('use').get_attribute('fill')
        pattern = translate_pattern(pattern)

        shape = card_elements[0].find_element_by_css_selector('use').get_attribute('href')
        shape = translate_shape(shape)

        card_array.append([card, number, color, pattern, shape])

    return card_array


#%% Evaluate Cards and return objects
def evaluate_cards(_cards):
    results = []

    for c in combinations(_cards, 3):
        val = 0
        for i in range(1, 5):
            if (c[0][i] == c[1][i] == c[2][i]) or (len(set([c[0][i], c[1][i], c[2][i]]))==3):
                val += 1
        if val == 4:
            results.append(c)

    return results


#%% Solve an individual game currently on page
def solve_game(window):
    cards = organize_cards(window.find_elements_by_class_name('set-board-card'))
    sets = evaluate_cards(cards)

    for s in sets:
        for c in s:
            c[0].click()
    sleep(1)


#%% Initialize Browser
browser = Firefox()

browser.get('https://www.nytimes.com/puzzles/set')
#Scroll away from banner ad
browser.execute_script("window.scrollTo(0, 400)")
sleep(1)


#%% Select each tab and solve the game.
for i in range(4):
    solve_game(browser)
    try:
        browser.find_element_by_class_name('pzm-modal__button').click()
    except:
        pass