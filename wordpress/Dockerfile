# Use a imagem base do PHP com Apache
FROM php:7.4-apache

# Atualize o sistema e instale as dependências necessárias
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libmcrypt-dev \
    libpng-dev \
    libzip-dev \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Configure as extensões do PHP
RUN docker-php-ext-install -j$(nproc) \
    bcmath \
    gd \
    mysqli \
    opcache \
    zip

# Baixe e instale o WordPress
RUN wget https://wordpress.org/latest.tar.gz && tar -xvzf latest.tar.gz -C /var/www/html --strip-components=1 && rm latest.tar.gz

# Copie o arquivo de configuração do WordPress
COPY wp-config.php /var/www/html/wp-config.php

# Configure as permissões adequadas
RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html

# Defina a diretiva de URL amigável do Apache
RUN a2enmod rewrite

# Exponha a porta do Apache
EXPOSE 80

# Inicie o Apache em segundo plano
CMD ["apache2-foreground"]
