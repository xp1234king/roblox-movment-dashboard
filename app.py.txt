local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

local CHECK_INTERVAL = 2
local STATIONARY_THRESHOLD = 0.1
local REPORT_URL = "https://roblox-movment-dashboard-1.onrender.com"

local lastPositions = {}

while true do
	local report = {}
	for _, player in ipairs(Players:GetPlayers()) do
		local char = player.Character
		if char and char:FindFirstChild("HumanoidRootPart") then
			local pos = char.HumanoidRootPart.Position
			local last = lastPositions[player.UserId]
			local moving = true
			if last then
				local dist = (pos - last).Magnitude
				moving = dist >= STATIONARY_THRESHOLD
			end
			lastPositions[player.UserId] = pos
			report[player.Name] = moving
		end
	end

	local payload = {
		serverId = game.JobId,
		gameId = game.GameId,
		players = report,
	}

	local json = HttpService:JSONEncode(payload)
	HttpService:PostAsync(REPORT_URL, json, Enum.HttpContentType.ApplicationJson)

	task.wait(CHECK_INTERVAL)
end
