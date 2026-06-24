import { createApp } from 'vue'
import { createPinia } from 'pinia'

import PrimeVue from 'primevue/config'
import { definePreset } from '@primeuix/themes'
import Aura from '@primeuix/themes/aura'

const CyberTwinPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: '{sky.50}', 100: '{sky.100}', 200: '{sky.200}', 300: '{sky.300}',
      400: '{sky.400}', 500: '{sky.500}', 600: '{sky.600}', 700: '{sky.700}',
      800: '{sky.800}', 900: '{sky.900}', 950: '{sky.950}',
    },
  },
})
import ConfirmationService from 'primevue/confirmationservice'
import ToastService from 'primevue/toastservice'
import Tooltip from 'primevue/tooltip'

import 'primeicons/primeicons.css'
import './assets/main.css'

import App from './App.vue'
import router from './router'

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Password from 'primevue/password'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import MultiSelect from 'primevue/multiselect'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import ConfirmDialog from 'primevue/confirmdialog'
import Toast from 'primevue/toast'
import Card from 'primevue/card'
import Tag from 'primevue/tag'
import Chart from 'primevue/chart'
import Avatar from 'primevue/avatar'
import Menu from 'primevue/menu'
import Message from 'primevue/message'
import ProgressSpinner from 'primevue/progressspinner'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Divider from 'primevue/divider'
import Popover from 'primevue/popover'
import Badge from 'primevue/badge'
import AutoComplete from 'primevue/autocomplete'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(PrimeVue, {
  theme: { preset: CyberTwinPreset, options: { darkModeSelector: '.app-dark', cssLayer: false } },
})
app.use(ConfirmationService)
app.use(ToastService)
app.directive('tooltip', Tooltip)

app.component('Button', Button)
app.component('InputText', InputText)
app.component('InputNumber', InputNumber)
app.component('Password', Password)
app.component('Textarea', Textarea)
app.component('Select', Select)
app.component('MultiSelect', MultiSelect)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Dialog', Dialog)
app.component('ConfirmDialog', ConfirmDialog)
app.component('Toast', Toast)
app.component('Card', Card)
app.component('Tag', Tag)
app.component('Chart', Chart)
app.component('Avatar', Avatar)
app.component('Menu', Menu)
app.component('Message', Message)
app.component('ProgressSpinner', ProgressSpinner)
app.component('IconField', IconField)
app.component('InputIcon', InputIcon)
app.component('Divider', Divider)
app.component('Popover', Popover)
app.component('Badge', Badge)
app.component('AutoComplete', AutoComplete)

import { useUiStore } from '@/stores/ui.store'
useUiStore(pinia).appliquerTheme()

app.mount('#app')
