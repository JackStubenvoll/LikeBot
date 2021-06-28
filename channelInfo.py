class channelInfoClass:
  white = []
  black = []
  whitelisted = True
  def __init__(self, channel):
    self.channel = channel
    self.white = []
    self.black = []
    print("new channel")
  
  def whitelist(self, reaction):
    self.white.append(reaction)
    print("Whitelisting " + reaction)

  def unwhitelist(self, reaction):
    self.white.remove(reaction)

  def checkList(self, reaction):
    if self.whitelisted:
      print("whitelist mode")
      # print(reaction)
      # print(self.white)
      # print(type(reaction))
      # print(type(self.white))
      # print(str(reaction) in self.white)
      if str(reaction) in self.white:
        return True
      else:
        return False
    else:
      print("blacklist mode")
      if str(reaction) in self.black:
        return False
      else:
        return True
    
    
  def blacklist(self, reaction):
    self.black.append(reaction)

  def unblacklist(self, reaction):
    self.black.remove(reaction)

