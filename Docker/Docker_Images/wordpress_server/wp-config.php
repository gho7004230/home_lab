<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', '{database}' );

/** MySQL database username */
define( 'DB_USER', '{user}' );

/** MySQL database password */
define( 'DB_PASSWORD', '{password}' );

/** MySQL hostname */
define( 'DB_HOST', 'db' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'ioCz0P(av0W{2 o5nTnBZ3VyE7Y3:_c=iS(=1.Gj{%PHHb3`SvN;mSORcYT0`d}6' );
define( 'SECURE_AUTH_KEY',  'KO30YW25q{m38kX>/slC_o6K L9ta:oPgZR#!0Igm,pdY9!OQ9R16C&QT>bgZP28' );
define( 'LOGGED_IN_KEY',    'v8NrgNlpH7s|ahI7M9oxK r3lNhiz5N&A=6n@VCg9Jh^uY_pz)LIIcsgpD_6n7+/' );
define( 'NONCE_KEY',        'Oez%YIuu!y~s6*S1qfho8=j#6{zE[XzN!et7/M.CECCV^3{7;7wh]mT~*m6h65dR' );
define( 'AUTH_SALT',        'b*DHvZ?,_WA!z]Y(JRk]=FEAC@syQeR]~7BFx5S-7Te7a%i$KE0<FB4QlD+&BP1Q' );
define( 'SECURE_AUTH_SALT', '!< ?gL2J9oSL![tX{0~]=!B0X7Z|fR+5o31K$A8O4OsYe2VBjFc>W$llGtO^r2e2' );
define( 'LOGGED_IN_SALT',   '3LMl 8$B=]Drltkp!1uKRf.6;FPePzFh|Q xKr`1=-*qx6bO>I,fp5FsaQ1r(%:}' );
define( 'NONCE_SALT',       '7kK/Wn+9/v1H|b4Z}hbEUPg)gZ9`acqJ%_Z/w!b>B&3Fx@[zqr4Eh+N,;_fmO^%2' );

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
        define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';

@ini_set('upload_max_size' , '256M' );
