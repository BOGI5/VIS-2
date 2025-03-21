// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/ui',
  ],
  ssr: false,
  devtools: { enabled: true },
  app: {
    head: {
      title: 'Title',
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
    },
  },
  css: ['bootstrap/dist/css/bootstrap.min.css'],
  compatibilityDate: '2024-11-01',
  eslint: {
    config: {
      stylistic: { indent: 2, quotes: 'single', semi: false },
    },
  },
})
