module.exports = {
  log: function (tag, arg) {
    console.log(tag, arg)
  },
  info: function (tag, arg) {
    console.info(tag, arg)
  },
  error: function (tag, arg) {
    console.error(tag, arg)
  }
}