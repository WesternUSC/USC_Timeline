let gulp = require('gulp')
let sass = require('gulp-sass')

function processSass() {
    return gulp
        .src('usctimeline/static/styles/scss/main.scss')
        .pipe(sass())
        .pipe(gulp.dest('usctimeline/static/styles/'))
}

function watch() {
    gulp.watch('usctimeline/static/styles/scss/**/*.scss', gulp.series(processSass))
}

gulp.task('sass', processSass)
gulp.task('watch', watch)
gulp.task('default', gulp.series(processSass, watch))
