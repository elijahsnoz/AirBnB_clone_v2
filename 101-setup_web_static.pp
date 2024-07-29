# Install Nginx package
package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
}

# Create necessary directories and files
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
  require => File['/data'],
}

file { '/data/web_static/releases':
  ensure => 'directory',
  require => File['/data/web_static'],
}

file { '/data/web_static/shared':
  ensure => 'directory',
  require => File['/data/web_static/releases'],
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  require => File['/data/web_static/releases'],
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>",
  require => File['/data/web_static/releases/test'],
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  require => File['/data/web_static/releases/test/index.html'],
}

# Set ownership of the /data/ directory
exec { 'chown -R ubuntu:ubuntu /data/':
  path    => ['/bin', '/usr/bin'],
  require => File['/data/web_static/current'],
}

# Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => template('nginx/default.erb'),
  require => Package['nginx'],
  notify  => Exec['nginx-restart'],
}

# Restart Nginx to apply changes
exec { 'nginx-restart':
  command     => '/usr/sbin/service nginx restart',
  refreshonly => true,
}
