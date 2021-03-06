# Данный код опубликовывает изображения с комиксами в вашу группу вконтакте

### Описание

Программа скачивает комикс с сайта [xkcd](https://xkcd.com/json.html), сохраняет в вашу папку и опубликовывает его в вашу группу вконтакте

### Установка

Python должен быть установлен. Затем используйте pip (или pip3 если есть конфликт с Python2) для установки зависимостей. Затем создайте виртуальное окружение и в терминале выполните команду по установке зависимостей:

```
pip install -r requirements.txt
```

### Переменные окружения

Для работы с API вконтакте нужно создать приложение по [ссылке](https://vk.com/editapp?act=create) и добавить ID вашего приложения в формате

`VK_APP_ID=id_приложения`

Необходимо добавить токен авторизации от вашего аккаунта вконтакте, получите его по [инструкции](https://vkhost.github.io/) и добавьте в формате

`VK_ACCESS_TOKEN=токен_авторизации`

Для публикации изображений в вашу группу вконтакте нужно создать [ее](https://vk.com/groups?w=groups_create) и добавить ID [группы](https://regvk.com/id/)

`VK_GROUP_ID=id_группы`

Укажите адрес по которому сохраняются изображения

`IMAGE_PATH=папка`

### Запуск

Для запуска программы введите в терминале команду:

```
python uploading_images.py
```



