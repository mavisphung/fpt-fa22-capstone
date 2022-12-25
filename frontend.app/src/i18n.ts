import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';
import enTranslation from './translation/en.json'
import viTranslation from './translation/vi.json'
const resources =  {
    en: {
        translation: enTranslation,
    },
    vi: {
        translation: viTranslation,
    }
}

i18next.use(initReactI18next).init({
    resources,
    lng: "vi",
});

export default i18next;