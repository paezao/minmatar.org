import { useTranslations, useTranslatedPath } from '@i18n/utils'
import { is_prod_mode } from '@helpers/env'
import type { Character } from '@dtypes/api.minmatar.org'
import { get_primary_characters } from '@helpers/api.minmatar.org/characters'

const ONE_DAY_IN_MS = 24*60*60*1000

export const onRequest = async ({ locals, cookies, request }, next) => {
    console.log(request.url)
    const lang = 'en'
    const t = useTranslations(lang);
    const translatePath = useTranslatedPath(lang);

    const auth_token = cookies.has('auth_token') ? cookies.get('auth_token').value : false

    const url = new URL(request.url)

    if (url.pathname == translatePath('/redirects/add_primary_character'))
        return next()

    if (cookies.has('auth_token') && !cookies.has('primary_pilot')) {
        let primary_pilot:Character
        let get_primary_characters_error = false;

        try {
            primary_pilot = await get_primary_characters(auth_token as string);

            if (primary_pilot?.character_id) {
                const in_1_day = new Date(new Date().getTime()+(ONE_DAY_IN_MS))
                cookies.set('primary_pilot', JSON.stringify(primary_pilot), { path: '/', expires: in_1_day })
            }
        } catch (error) {
            get_primary_characters_error = (is_prod_mode() ? t('get_primary_characters_error') : error.message)
            cookies.set('middleware_error', get_primary_characters_error, { path: '/' })
            console.log(get_primary_characters_error)
        }
    }

    return next();
};