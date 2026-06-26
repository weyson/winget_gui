"""国际化(i18n)模块"""
import json
import os
import locale
from typing import Dict, Optional


class I18n:
    """国际化管理类"""
    
    SUPPORTED_LANGUAGES = {
        'zh_CN': {'code': 'zh_CN', 'name': '简体中文', 'english_name': 'Chinese (Simplified)'},
        'zh_TW': {'code': 'zh_TW', 'name': '繁体中文', 'english_name': 'Chinese (Traditional)'},
        'en': {'code': 'en', 'name': 'English', 'english_name': 'English'},
        'ru': {'code': 'ru', 'name': 'Русский', 'english_name': 'Russian'},
        'ja': {'code': 'ja', 'name': '日本語', 'english_name': 'Japanese'},
        'ko': {'code': 'ko', 'name': '한국어', 'english_name': 'Korean'}
    }
    
    DEFAULT_LANGUAGE = 'zh_CN'
    
    def __init__(self):
        self._current_lang = None
        self._translations = {}
        self._config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self._locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
        
        self._load_config()
        self._load_translations()
    
    def _load_config(self):
        """加载用户配置"""
        if os.path.exists(self._config_path):
            try:
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    user_lang = config.get('language')
                    if user_lang in self.SUPPORTED_LANGUAGES:
                        self._current_lang = user_lang
                        return
            except Exception:
                pass
        
        self._current_lang = self._detect_system_language()
    
    def _detect_system_language(self) -> str:
        """检测系统默认语言"""
        try:
            lang_code, _ = locale.getdefaultlocale()
            if lang_code:
                if lang_code.startswith('zh_CN') or lang_code.startswith('zh-Hans'):
                    return 'zh_CN'
                elif lang_code.startswith('zh_TW') or lang_code.startswith('zh-Hant'):
                    return 'zh_TW'
                elif lang_code.startswith('en'):
                    return 'en'
                elif lang_code.startswith('ru'):
                    return 'ru'
                elif lang_code.startswith('ja'):
                    return 'ja'
                elif lang_code.startswith('ko'):
                    return 'ko'
        except Exception:
            pass
        
        return self.DEFAULT_LANGUAGE
    
    def _load_translations(self):
        """加载翻译文件"""
        try:
            lang_file = os.path.join(self._locales_dir, f'{self._current_lang}.json')
            with open(lang_file, 'r', encoding='utf-8') as f:
                self._translations = json.load(f)
        except Exception:
            self._translations = {}
    
    def _save_config(self):
        """保存用户配置"""
        try:
            config = {'language': self._current_lang}
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def set_language(self, lang_code: str):
        """设置语言"""
        if lang_code in self.SUPPORTED_LANGUAGES:
            self._current_lang = lang_code
            self._load_translations()
            self._save_config()
    
    def get_language(self) -> str:
        """获取当前语言代码"""
        return self._current_lang
    
    def get_language_name(self) -> str:
        """获取当前语言名称"""
        return self.SUPPORTED_LANGUAGES.get(self._current_lang, {}).get('name', '')
    
    def t(self, key: str, **kwargs) -> str:
        """获取翻译文本"""
        text = self._translations.get(key, key)
        
        if kwargs:
            try:
                text = text.format(**kwargs)
            except Exception:
                pass
        
        return text
    
    def get_supported_languages(self) -> Dict[str, Dict]:
        """获取所有支持的语言"""
        return self.SUPPORTED_LANGUAGES.copy()