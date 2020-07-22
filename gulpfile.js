let gulp = require('gulp')
let sass = require('gulp-sass')

function processSass() {
    return gulp
        .src('static/styles/scss/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('static/styles/css'))
}

function watch() {
    gulp.watch('static/styles/scss/*.scss', processSass)
}

gulp.task('sass', processSass)
gulp.task('watch', watch)
gulp.task('default', gulp.series(processSass, watch))
