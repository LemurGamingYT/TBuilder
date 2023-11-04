using Terraria.DataStructures;
using Microsoft.Xna.Framework;
using Terraria.ModLoader;
using Terraria.Audio;
using Terraria.ID;
using Terraria;
using System;


public class Utility
{
    /// <summary>
    /// Provides a more concise way to find an <see cref="NPC"/>'s target
    /// </summary>
    /// <param name="npc">The npc</param>
    /// <returns><see langword="null"/> if the player is dead or something else happened, otherwise,
    /// a <see cref="Player"/> target</returns>
    public static Player FindTarget(NPC npc)
    {
        if (npc.target < 0 || npc.target == 255 || Main.player[npc.target].dead || !Main.player[npc.target].active)
        {
            npc.TargetClosest();
        }

        Player player = Main.player[npc.target];
        return player.dead ? null : player;
    }

    /// <summary>
    /// Provides a more concise way to find a projectile homing target
    /// </summary>
    /// <param name="projectile">The <see cref="Projectile"/></param>
    /// <param name="withinRange">The range in which the projectile can 'see' a target</param>
    /// <param name="seeThroughBlocks">Whether the projectile can see through solid blocks</param>
    /// <returns>An <see cref="NPC"/> target or null if no target was found</returns>
    public static NPC FindTarget(Projectile projectile, float withinRange = 10f, bool seeThroughBlocks = true)
    {
        // seeThroughBlocks is the opposite of checkCanHit, so invert the boolean
        return projectile.FindTargetWithinRange(withinRange, !seeThroughBlocks);
    }

    /// <summary>
    /// Converts a <see cref="Vector2"/> to a rotation <see cref="float"/>
    /// </summary>
    /// <param name="v">The <see cref="Vector2"/> to be converted to </param>
    /// <returns>The rotation <see cref="float"/> from the <see cref="Vector2"/></returns>
    public static float ToRotation(Vector2 v)
    {
        return v.ToRotation() - MathHelper.PiOver2;
    }

    /// <summary>
    /// The default collision. Plays the default tile hit sound and uses <see cref="Collision.HitTiles"/>
    /// </summary>
    /// <param name="position">The position of the collision</param>
    /// <param name="velocity">The velocity of the collision</param>
    /// <param name="width">The width of the collision</param>
    /// <param name="height">The height of the collision</param>
    public static void DefaultCollide(Vector2 position, Vector2 velocity, int width, int height)
    {
        Collision.HitTiles(position, velocity, width, height);
        SoundEngine.PlaySound(SoundID.Item10, position);
    }

    /// <summary>
    /// Turns the <see cref="NPC"/>'s <see cref="NPC.spriteDirection"/> to face the <see cref="Player"/>
    /// </summary>
    /// <param name="npc">The <see cref="NPC"/></param>
    /// <param name="player">The <see cref="Player"/></param>
    public static void FaceTargetX(NPC npc, Player player)
    {
        npc.spriteDirection = player.Center.X > npc.Center.X ? 1 : -1;
    }

    /// <summary>
    /// Turns the <see cref="Projectile"/>'s <see cref="Projectile.spriteDirection"/> to face the <see cref="NPC"/> target
    /// </summary>
    /// <param name="projectile">The <see cref="Projectile"/></param>
    /// <param name="target">The <see cref="NPC"/></param>
    public static void FaceTargetX(Projectile projectile, NPC target)
    {
        projectile.spriteDirection = target.Center.X > projectile.Center.X ? 1 : -1;
    }

    /// <summary>
    /// Scale the expert stats for <see cref="NPC"/> bosses
    /// </summary>
    /// <param name="npc">The <see cref="NPC"/></param>
    /// <param name="balance">From the <see cref="ModNPC.ApplyDifficultyAndPlayerScaling"/> method</param>
    /// <param name="bossAdjustment">From the <see cref="ModNPC.ApplyDifficultyAndPlayerScaling"/> method</param>
    public static void ScaleStats(NPC npc, float balance, float bossAdjustment)
    {
        npc.lifeMax = (int)(npc.lifeMax * balance * bossAdjustment / 1.25);
        npc.life = (int)(npc.life * balance * bossAdjustment / 1.25);

        npc.damage = (int)(npc.damage * balance * bossAdjustment / 1.25);
    }

    /// <param name="position">The current position e.g. from the <see cref="NPC"/></param>
    /// <param name="targetPosition">The current position e.g. from the <see cref="NPC"/></param>
    /// <returns>The literal rotation <see cref="float"/></returns>
    public static float FaceTarget(Vector2 position, Vector2 targetPosition)
    {
        return RotatationTo(targetPosition, position);
    }

    /// <summary>
    /// Advanced spawning of a projectile
    /// </summary>
    /// <param name="source">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="position">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="velocity">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="type">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="damage">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="knockback">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="friendly">Changes <see cref="Projectile.friendly"/></param>
    /// <param name="hostile">Changes <see cref="Projectile.hostile"/></param>
    /// <param name="owner">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="ai0">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="ai1">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="ai2">Same as <see cref="Projectile.NewProjectile"/></param>
    /// <param name="timeLeft">Changes <see cref="Projectile.timeLeft"/></param>
    /// <param name="rotation">Changes <see cref="Projectile.rotation"/></param>
    /// <param name="netUpdate">Changes <see cref="Projectile.netUpdate"/></param>
    /// <param name="tileCollide">Changes <see cref="Projectile.tileCollide"/></param>
    /// <param name="penetrate">Changes <see cref="Projectile.penetrate"/></param>
    /// <returns>The generated <see cref="Projectile"/></returns>
    public static Projectile AdvancedSpawnProjectile(IEntitySource source, Vector2 position, Vector2 velocity, int type,
        int damage, float knockback, bool friendly = false, bool hostile = true, int owner = -1, float ai0 = 0,
        float ai1 = 0, float ai2 = 0, int timeLeft = 300, float rotation = 0, bool netUpdate = true,
        bool tileCollide = true, int penetrate = -1)
    {
        if (Main.netMode != NetmodeID.MultiplayerClient)
        {
            Projectile projectile = Main.projectile[Projectile.NewProjectile(source, position, velocity, type, damage,
                knockback, owner, ai0, ai1, ai2)];
            projectile.friendly = friendly;
            projectile.hostile = hostile;
            projectile.timeLeft = timeLeft;
            projectile.rotation = rotation;
            projectile.netUpdate = netUpdate;
            projectile.tileCollide = tileCollide;
            projectile.penetrate = penetrate;

            return projectile;
        }

        return null;
    }

    /// <summary>
    /// Advanced spawning of <see cref="NPC"/>
    /// </summary>
    /// <param name="source">Same as <see cref="NPC.NewNPC"/></param>
    /// <param name="position">Same as <see cref="NPC.NewNPC"/>'s X and Y parameters but into one parameter</param>
    /// <param name="velocity">Changes <see cref="NPC"/>'s velocity</param>
    /// <param name="type">Same as <see cref="NPC.NewNPC"/></param>
    /// <param name="target">Same as <see cref="NPC.NewNPC"/></param>
    /// <param name="ai0">Same as <see cref="NPC.NewNPC"/></param>
    /// <param name="ai1">Same as <see cref="NPC.NewNPC"/></param>
    /// <param name="ai2">Same as <see cref="NPC.NewNPC"/></param>
    /// <param name="ai3">Same as <see cref="NPC.NewNPC"/></param>
    /// <param name="start">Same as <see cref="NPC.NewNPC"/></param>
    /// <returns></returns>
    public static NPC AdvancedSpawnNPC(IEntitySource source, Vector2 position, Vector2 velocity, int type, int target = 255,
        int ai0 = 0, int ai1 = 0, int ai2 = 0, int ai3 = 0, int start = 0, int netId = -1)
    {
        NPC npc = Main.npc[NPC.NewNPC(source, (int)position.X, (int)position.Y, type, start, ai0, ai1, ai2, ai3, Target: target)];
        npc.velocity = velocity;
        npc.netID = netId;
        return npc;
    }

    /// <summary>
    /// Advanced spawning of <see cref="Dust"/>
    /// </summary>
    /// <param name="position">Same as <see cref="Dust.NewDust"/></param>
    /// <param name="width">Same as <see cref="Dust.NewDust"/></param>
    /// <param name="height">Same as <see cref="Dust.NewDust"/></param>
    /// <param name="type">Same as <see cref="Dust.NewDust"/></param>
    /// <param name="speedX">Same as <see cref="Dust.NewDust"/></param>
    /// <param name="speedY">Same as <see cref="Dust.NewDust"/></param>
    /// <param name="alpha">Same as <see cref="Dust.NewDust"/></param>
    /// <param name="color">Same as <see cref="Dust.NewDust"/></param>
    /// <param name="scale">Same as <see cref="Dust.NewDust"/></param>
    /// <param name="noLight">Changes <see cref="Dust.noLight"/></param>
    /// <param name="fadeIn">Changes <see cref="Dust.fadeIn"/></param>
    /// <param name="noLightEmittence">Changes <see cref="Dust.noLightEmittence"/></param>
    /// <param name="noGravity">Changes <see cref="Dust.noGravity"/></param>
    /// <param name="rotation">Changes <see cref="Dust.rotation"/></param>
    /// 
    /// <returns>The generated <see cref="Dust"/></returns>
    public static Dust AdvancedSpawnDust(Vector2 position, int width, int height, int type, float speedX = 0,
        float speedY = 0, int alpha = 0, Color color = default, float scale = 1, bool noLight = true, int fadeIn = 0,
        bool noLightEmittence = true, bool noGravity = true, float rotation = 0)
    {
        Dust dust = Main.dust[Dust.NewDust(position, width, height, type, speedX, speedY, alpha, color, scale)];
        dust.noLightEmittence = noLightEmittence;
        dust.noGravity = noGravity;
        dust.rotation = rotation;
        dust.noLight = noLight;
        dust.fadeIn = fadeIn;

        return dust;
    }

    /// <summary>
    /// Gets the rotation from the start to position
    /// </summary>
    /// <param name="start">The starting <see cref="Vector2"/></param>
    /// <param name="position">The target <see cref="Vector2"/></param>
    /// <returns>The rotation <see cref="float"/></returns>
    public static float RotatationTo(Vector2 start, Vector2 position)
    {
        Vector2 r = start - position;
        return (float)Math.Atan2(r.Y, r.X) - MathHelper.PiOver2;
    }

    /// <summary>
    /// Provides an easier way for the <see cref="NPC"/> to move towards the <see cref="Player"/>
    /// </summary>
    /// <param name="npc">The <see cref="NPC"/></param>
    /// <param name="player">The <see cref="Player"/></param>
    /// <param name="speed">The speed <see cref="float"/> at which the <see cref="NPC"/> will move towards
    /// the <see cref="Player"/></param>
    public static void MoveTowards(NPC npc, Player player, float speed)
    {
        Vector2 move = player.Center - npc.Center;

        float mag = (float)Math.Sqrt(move.X * move.X + move.Y * move.Y);
        move *= speed / mag;

        npc.velocity = move;
    }

    /// <param name="npc">The <see cref="NPC"/></param>
    /// <param name="requiredHealth">The required health <see cref="int"/></param>
    /// <returns><see langword="true"/> if the <see cref="NPC.life"/> is less than <see cref="NPC.lifeMax"/> divided
    /// by the requiredHealth parameter</returns>
    public static bool ChangePhase(NPC npc, int requiredHealth)
    {
        return npc.life <= (npc.lifeMax / requiredHealth);
    }

    /// <summary>
    /// Changes <see cref="NPC.frame"/> count
    /// </summary>
    /// <param name="npc">The <see cref="NPC"/></param>
    /// <param name="maxFrames">The maximum frames <see cref="int"/></param>
    /// <param name="frameHeight">Provided by <see cref="ModNPC.FindFrame"/></param>
    /// <param name="startFrame">Starting frame</param>
    /// <param name="frameSpeed">The amount of time spent on each animation frame</param>
    public static void FindFrame(NPC npc, int maxFrames, int frameHeight, int startFrame = 0, int frameSpeed = 5)
    {
        int finalFrame = maxFrames - 1;

        npc.frameCounter += 0.5f;
        // Loop through the 4 animation frames, spending 5 ticks on each
        if (npc.frameCounter > frameSpeed)
        {
            npc.frameCounter = 0;
            npc.frame.Y += frameHeight;

            if (npc.frame.Y > finalFrame * frameHeight)
            {
                npc.frame.Y = startFrame * frameHeight;
            }
        }
    }

    /// <summary>
    /// Changes <see cref="Projectile.frame"/>
    /// </summary>
    /// <param name="projectile">The <see cref="Projectile"/></param>
    /// <param name="maxFrames">The maximum frames <see cref="int"/></param>
    /// <param name="ticksOnEach">The amount of time spent on each animation frame</param>
    public static void FindFrame(Projectile projectile, int maxFrames = -1, int ticksOnEach = 5)
    {
        if (maxFrames == -1)
        {
            maxFrames = Main.projFrames[projectile.type];
        }

        // Loop through the 4 animation frames, spending 5 ticks on each
        // Projectile.frame — index of current frame
        if (++projectile.frameCounter >= ticksOnEach)
        {
            projectile.frameCounter = 0;
            // Compact version: Projectile.frame = ++Projectile.frame % maxFrames;
            if (++projectile.frame >= maxFrames)
                projectile.frame = 0;
        }
    }

    /// <param name="start">The starting position (e.g. the NPC's position)</param>
    /// <param name="towards">The end position (e.g. the Player's position)</param>
    /// <param name="speed">The speed at which it should travel</param>
    /// <returns>A Vector2 to move toward the target position at the speed</returns>
    public static Vector2 TowardPos(Vector2 start, Vector2 towards, float speed)
    {
        return (towards - start).SafeNormalize(Vector2.UnitX) * speed;
    }

    /// <summary>
    /// Checks if the current random float is greater than chance
    /// </summary>
    /// <param name="chance">The chance to not consume ammo, e.g. .4f would be 40%</param>
    /// <returns>A boolean whether the current random float is greater than chance</returns>
    public static bool ShouldConsumeAmmo(float chance)
    {
        if (Main.rand.NextFloat() > chance)
        {
            return true;
        }

        return false;
    }

    /// <summary>
    /// Resets the timer if it goes over the maxTimer
    /// </summary>
    /// <param name="timer">The current timer</param>
    /// <param name="maxTimer">The max timer</param>
    /// <returns></returns>
    public static int UpdateTimer(int timer, int maxTimer)
    {
        return timer >= maxTimer ? 0 : timer + 1;
    }

    /// <summary>
    /// Converts tiles to <see cref="float"/> for use in functions
    /// </summary>
    /// <param name="tiles">The amount of tiles</param>
    /// <returns>The converted <see cref="float"/></returns>
    public static float ToFloat(float tiles)
    {
        // Terraria is 16x16 pixels so times by 16 to get the distance
        return tiles * 16;
    }

    /// <summary>
    /// Converts <see cref="float"/> to tiles for use in functions
    /// </summary>
    /// <param name="f">The <see cref="float"/></param>
    /// <returns>To the tile</returns>
    public static float ToTile(float f)
    {
        return f / 16;
    }

    /// <summary>
    /// Function to multiply item damage
    /// </summary>
    /// <param name="dmg">The current damage</param>
    /// <param name="by">The amount of damage to multiply by</param>
    /// <returns>An integer multiplied by the by parameter</returns>
    public static int MultiplyDamage(int dmg, float by)
    {
        return (int)(dmg * by);
    }

    /// <summary>
    /// Checks if the x and y are valid in inside the world
    /// </summary>
    /// <param name="x">The x coordinate</param>
    /// <param name="y">The y coordinate</param>
    /// <returns>A boolean to check if the position is within the world</returns>
    public static bool WithinWorld(int x, int y)
    {
        return x >= 0 && x < Main.maxTilesX && y >= 0 && y < Main.maxTilesY;
    }

    /// <summary>
    /// Makes the projectile bounce
    /// </summary>
    /// <param name="projectile">The <see cref="Projectile"/> to make bounce</param>
    /// <param name="oldVelocity">The oldVelocity, given by <see cref="ModProjectile.OnTileCollide"/></param>
    public static void Bounce(Projectile projectile, Vector2 oldVelocity)
    {
        // If the projectile hits the left or right side of the tile, reverse the X velocity
        if (Math.Abs(projectile.velocity.X - oldVelocity.X) > float.Epsilon)
        {
            projectile.velocity.X = -oldVelocity.X;
        }

        // If the projectile hits the top or bottom side of the tile, reverse the Y velocity
        if (Math.Abs(projectile.velocity.Y - oldVelocity.Y) > float.Epsilon)
        {
            projectile.velocity.Y = -oldVelocity.Y;
        }
    }
}
