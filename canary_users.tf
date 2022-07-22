
resource "aws_iam_user" "ggcanary_users" {
  for_each = var.users
  name     = "${var.global_prefix}_${each.key}"
  path     = "/ggcanary/"
  tags     = each.value
}

resource "aws_iam_access_key" "ggcanary_keys" {
  for_each   = var.users
  user       = aws_iam_user.ggcanary_users[each.key].name
  depends_on = [aws_iam_user.ggcanary_users]
}
