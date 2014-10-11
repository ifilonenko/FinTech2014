module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    includes: {
      files: {
        src: ['source/html/index.html'], // Source files
        dest: '.', // Destination directory
        flatten: true,
        cwd: '.',
        options: {
          silent: true,
          banner: '<!-- I am a banner <% includes.files.dest %> -->'
        }
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-includes');

  // Default task(s).
  grunt.registerTask('default', ['includes']);

};
