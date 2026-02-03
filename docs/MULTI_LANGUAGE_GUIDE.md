# Multi-Language Support Guide

## Overview
Mohi ERP now supports multiple Indian languages using Flask-Babel for internationalization (i18n).

## Supported Languages
- 🇬🇧 **English** (en) - Default
- 🇮🇳 **हिंदी** (hi) - Hindi
- 🇮🇳 **ગુજરાતી** (gu) - Gujarati
- 🇮🇳 **मराठी** (mr) - Marathi
- 🇮🇳 **தமிழ்** (ta) - Tamil

## Features
✅ Language switcher in navigation bar
✅ Automatic browser language detection
✅ Session-based language persistence
✅ All UI elements translated
✅ Number and currency formatting
✅ Date and time localization
✅ RTL support for regional scripts

---

## Installation

### 1. Install Dependencies
```bash
pip install Flask-Babel==4.0.0
```

### 2. Initialize Babel
```bash
# Extract translatable strings from code
pybabel extract -F babel.cfg -o messages.pot .

# Initialize translations for each language
pybabel init -i messages.pot -d app/translations -l hi
pybabel init -i messages.pot -d app/translations -l gu
pybabel init -i messages.pot -d app/translations -l mr
pybabel init -i messages.pot -d app/translations -l ta

# Compile translations
pybabel compile -d app/translations
```

### 3. Update Translations
After adding new translatable strings:
```bash
# Extract new strings
pybabel extract -F babel.cfg -o messages.pot .

# Update existing translations
pybabel update -i messages.pot -d app/translations

# Edit .po files in app/translations/*/LC_MESSAGES/messages.po

# Compile updated translations
pybabel compile -d app/translations
```

---

## Usage

### In Templates (Jinja2)
```html
<!-- Simple translation -->
<h1>{{ _('Dashboard') }}</h1>

<!-- Translation with variables -->
<p>{{ _('Welcome, %(name)s!', name=user.name) }}</p>

<!-- Plural forms -->
<p>{{ ngettext('%(num)d item', '%(num)d items', count) }}</p>
```

### In Python Code
```python
from flask_babel import gettext, ngettext

# Simple translation
message = gettext('Order created successfully')

# Translation with variables
message = gettext('Total amount: %(amount)s', amount=total)

# Plural forms
message = ngettext('%(num)d product', '%(num)d products', count)
```

### Number Formatting
```python
from flask_babel import format_currency, format_number, format_decimal

# Currency
amount = format_currency(25000, 'INR', locale='hi_IN')  # ₹25,000

# Numbers
number = format_number(1234567, locale='hi_IN')  # 12,34,567

# Decimals
decimal = format_decimal(123.45, locale='hi_IN')  # 123.45
```

### Date Formatting
```python
from flask_babel import format_date, format_datetime

# Date
date = format_date(datetime.now(), format='medium', locale='hi')

# DateTime
datetime_str = format_datetime(datetime.now(), format='medium', locale='hi')
```

---

## Language Switcher

### How It Works
1. User clicks language dropdown (🌐 icon)
2. Selects preferred language
3. Language stored in session
4. Page reloads with new language
5. All text automatically translated

### URL
```
/language/set/<lang_code>
```

Example:
- `/language/set/hi` - Switch to Hindi
- `/language/set/gu` - Switch to Gujarati
- `/language/set/en` - Switch to English

---

## Translation Files Structure

```
app/
└── translations/
    ├── hi/
    │   └── LC_MESSAGES/
    │       ├── messages.po  (Edit this)
    │       └── messages.mo  (Compiled)
    ├── gu/
    │   └── LC_MESSAGES/
    │       ├── messages.po
    │       └── messages.mo
    ├── mr/
    │   └── LC_MESSAGES/
    │       ├── messages.po
    │       └── messages.mo
    └── ta/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

---

## Translation Workflow

### 1. Mark Strings for Translation
```python
# In Python
from flask_babel import gettext as _

@bp.route('/dashboard')
def dashboard():
    flash(_('Welcome to dashboard'), 'success')
    return render_template('dashboard.html', title=_('Dashboard'))
```

```html
<!-- In Templates -->
<h1>{{ _('Dashboard') }}</h1>
<button>{{ _('Save') }}</button>
```

### 2. Extract Strings
```bash
pybabel extract -F babel.cfg -o messages.pot .
```

### 3. Update Translation Files
```bash
pybabel update -i messages.pot -d app/translations
```

### 4. Translate
Edit `app/translations/hi/LC_MESSAGES/messages.po`:
```po
msgid "Dashboard"
msgstr "डैशबोर्ड"

msgid "Save"
msgstr "सहेजें"

msgid "Welcome, %(name)s!"
msgstr "स्वागत है, %(name)s!"
```

### 5. Compile
```bash
pybabel compile -d app/translations
```

### 6. Restart App
```bash
docker-compose restart web
```

---

## Common Translations

### Navigation
| English | Hindi | Gujarati | Marathi |
|---------|-------|----------|---------|
| Dashboard | डैशबोर्ड | ડેશબોર્ડ | डॅशबोर्ड |
| Orders | ऑर्डर | ઓર્ડર | ऑर्डर |
| Payments | भुगतान | ચુકવણી | देयके |
| Products | उत्पाद | ઉત્પાદનો | उत्पादने |
| Inventory | इन्वेंटरी | ઇન્વેન્ટરી | यादी |
| Accounting | लेखा | હિસાબ | लेखा |
| Analytics | विश्लेषण | વિશ્લેષણ | विश्लेषण |

### Actions
| English | Hindi | Gujarati | Marathi |
|---------|-------|----------|---------|
| Save | सहेजें | સાચવો | जतन करा |
| Cancel | रद्द करें | રદ કરો | रद्द करा |
| Delete | हटाएं | કાઢી નાખો | हटवा |
| Edit | संपादित करें | સંપાદિત કરો | संपादित करा |
| Add | जोड़ें | ઉમેરો | जोडा |
| Search | खोजें | શોધો | शोधा |
| Export | निर्यात | નિકાસ | निर्यात |
| Print | प्रिंट करें | છાપો | छापा |

### Status
| English | Hindi | Gujarati | Marathi |
|---------|-------|----------|---------|
| Pending | लंबित | બાકી | प्रलंबित |
| Completed | पूर्ण | પૂર્ણ | पूर्ण |
| Cancelled | रद्द | રદ | रद्द |
| Active | सक्रिय | સક્રિય | सक्रिय |
| Inactive | निष्क्रिय | નિષ્ક્રિય | निष्क्रिय |

---

## Configuration

### config.py
```python
# Multi-Language Support
LANGUAGES = {
    'en': 'English',
    'hi': 'हिंदी (Hindi)',
    'gu': 'ગુજરાતી (Gujarati)',
    'mr': 'मराठी (Marathi)',
    'ta': 'தமிழ் (Tamil)'
}
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'Asia/Kolkata'
BABEL_TRANSLATION_DIRECTORIES = 'translations'
```

### app/__init__.py
```python
from flask_babel import Babel

babel = Babel()

def get_locale():
    """Get user's preferred language"""
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(Config.LANGUAGES.keys())

def create_app():
    # ...
    babel.init_app(app, locale_selector=get_locale)
```

---

## Testing

### Test Language Switching
1. Open http://localhost:5000
2. Click language dropdown (🌐)
3. Select "हिंदी (Hindi)"
4. Verify UI changes to Hindi
5. Test all pages

### Test Browser Detection
1. Clear session cookies
2. Change browser language to Hindi
3. Open application
4. Should automatically show Hindi

### Test Persistence
1. Switch to Gujarati
2. Navigate to different pages
3. Language should remain Gujarati
4. Close and reopen browser
5. Language should still be Gujarati

---

## Troubleshooting

### Translations Not Showing
```bash
# Recompile translations
pybabel compile -d app/translations

# Restart application
docker-compose restart web
```

### New Strings Not Translated
```bash
# Extract and update
pybabel extract -F babel.cfg -o messages.pot .
pybabel update -i messages.pot -d app/translations

# Edit .po files
# Then compile
pybabel compile -d app/translations
```

### Language Not Persisting
- Check session configuration
- Ensure `session.permanent = True`
- Check SECRET_KEY is set

---

## Best Practices

### 1. Always Use Translation Functions
```python
# ❌ Bad
flash('Order created successfully')

# ✅ Good
flash(_('Order created successfully'))
```

### 2. Use Variables for Dynamic Content
```python
# ❌ Bad
message = _('Total: ') + str(amount)

# ✅ Good
message = _('Total: %(amount)s', amount=format_currency(amount, 'INR'))
```

### 3. Keep Strings Simple
```python
# ❌ Bad (hard to translate)
_('Click here to view your order history and track shipments')

# ✅ Good (split into smaller strings)
_('View order history')
_('Track shipments')
```

### 4. Use Context for Ambiguous Words
```python
# For "Order" (noun vs verb)
_('Order')  # noun
pgettext('verb', 'Order')  # verb
```

### 5. Test All Languages
- Test with actual users who speak the language
- Check text overflow in UI
- Verify RTL layout for scripts that need it
- Test number and date formats

---

## Future Enhancements

### Phase 5.1: More Languages
- [ ] Bengali (বাংলা)
- [ ] Telugu (తెలుగు) - Already added
- [ ] Kannada (ಕನ್ನಡ)
- [ ] Malayalam (മലയാളം)
- [ ] Punjabi (ਪੰਜਾਬੀ)

### Phase 5.2: Advanced Features
- [ ] User-specific language preference in database
- [ ] Language-specific PDF reports
- [ ] Email templates in user's language
- [ ] AI chat in regional languages
- [ ] Voice input in regional languages

### Phase 5.3: Localization
- [ ] Indian number formats (12,34,567)
- [ ] Regional date formats
- [ ] State-specific terminology
- [ ] Industry-specific translations

---

## Resources

### Official Documentation
- Flask-Babel: https://python-babel.github.io/flask-babel/
- Babel: http://babel.pocoo.org/
- Unicode CLDR: http://cldr.unicode.org/

### Translation Tools
- Poedit: https://poedit.net/ (GUI for editing .po files)
- Lokalize: https://userbase.kde.org/Lokalize
- Online: https://localise.biz/free/poeditor

### Indian Language Resources
- Google Translate API
- Microsoft Translator
- Bhashini (Government of India)

---

## Support

For translation help or issues:
1. Check this guide
2. Review Flask-Babel documentation
3. Test with `pybabel` commands
4. Check translation files syntax
5. Restart application

---

**Status:** Phase 5 - In Progress
**Last Updated:** January 26, 2026
**Version:** 5.0.0
