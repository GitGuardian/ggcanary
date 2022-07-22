
output "ggcanary_access_keys" {
  value = [
    for user_name, user in aws_iam_user.ggcanary_users :
    {
      name              = user_name
      tags              = user.tags
      access_key_id     = aws_iam_access_key.ggcanary_keys[user_name].id
      access_key_secret = aws_iam_access_key.ggcanary_keys[user_name].secret
    }
  ]
  sensitive = true
}
