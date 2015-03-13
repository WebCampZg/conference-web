/* jshint node:true */

module.exports = function ( grunt ) {

    grunt.initConfig({

        sass: {
            dist: {
                options: {
                    sourcemap: 'none',
                    style: 'expanded',
                    precision: 5,
                    loadPath: [
                        'node_modules/bourbon/app/assets/stylesheets'
                    ]
                },
                files: {
                    'static/stylesheets/site.css': 'static/stylesheets/source/index.scss'
                }
            }
        },

        cssmin: {
            dist: {
                options: {
                    keepSpecialComments: 0,
                    restructuring: false
                },
                files: {
                    'static/stylesheets/site.css': [
                        'node_modules/normalize.css/normalize.css',
                        'node_modules/rationalize.css/dist/rationalize.css',
                        'static/stylesheets/site.css'
                    ]
                }
            }
        },

        postcss: {
            dist: {
                options: {
                    map: false,
                    processors: [
                        require('autoprefixer-core')({ browsers: ['last 2 version'] }).postcss,
                        require('pixrem')(),
                        require('postcss-assets')(),
                    ]
                },
                src: 'static/stylesheets/site.css',
                dest: 'static/stylesheets/site.css'
            }
        },

        ttf2woff: {
            dist: {
                src: ['static/fonts/*.ttf'],
                dest: 'static/fonts/'
            }
        },

        imagemin: {
            main: {
                options: {
                    svgoPlugins: [
                        {removeTitle: true},
                        {removeDesc: true},
                        {removeUselessStrokeAndFill: false},
                        {removeViewBox: false},
                    ]
                },
                files: [{
                    expand: true,
                    cwd: 'static/images/',
                    src: [
                        '**/*.{png,jpg,gif,svg}'
                    ],
                    dest: 'static/images/'
                }]
            }
        },

        watch: {
            css: {
                files: ['static/stylesheets/source/**/*.scss'],
                tasks: ['css'],
                options: {
                    spawn: false
                }
            }
        },

        connect: {
            dev: {
                options: {
                    open: true
                }
            }
        },

        concurrent: {
            main: {
                options: {
                    logConcurrentOutput: true
                },
                tasks: ['watch:css', 'connect:dev:keepalive']
            }
        }

    });

    require('load-grunt-tasks')(grunt);

    grunt.registerTask('default', ['imagemin','css']);
    grunt.registerTask('css', ['sass','cssmin','postcss']);
    grunt.registerTask('font', ['ttf2woff']);
    grunt.registerTask('dev', ['default','concurrent']);

};
