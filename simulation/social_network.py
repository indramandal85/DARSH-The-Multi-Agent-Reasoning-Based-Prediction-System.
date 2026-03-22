# simulation/social_network.py
#
# AGENT-TO-AGENT SOCIAL INFLUENCE LAYER
#
# v1 problem: every agent received the same world_context string.
# Nobody actually read what other agents posted.
# The "social media simulation" was social in name only.
#
# v2 solution: each agent has a follower graph.
# Each round, agents post their thought.
# Before thinking, each agent reads posts from agents they follow.
# This creates real information cascades — emotional agents amplify panic,
# rational agents filter it, tribal agents create echo chambers.
#
# The follow graph is built at simulation start based on agent type.
# It's static within one simulation run (agents don't gain/lose followers).

import random


class SocialNetwork:
    """
    Manages the follower graph and post feed for a simulation.

    Architecture:
        followers[agent_id] = list of agent_ids this agent follows
        posts[agent_id]     = list of post strings from this round

    Called by SimulationRunner:
        1. network.build(agents)              — at simulation start
        2. network.post(agent_id, content)    — after each agent's think()
        3. feed = network.get_feed(agent_id)  — before each agent's think()
        4. network.clear_round_posts()        — after all agents finish a round
    """

    # How many agents each type follows (determines information exposure)
    # Emotional: many follows = highly influenced by others
    # Rational: few follows = more independent thinking
    # Tribal: follows mostly own type = echo chamber effect
    # Contrarian: follows diverse set = deliberately seeks opposing views
    # Institutional: follows institutional + rational = formal network
    FOLLOW_COUNTS = {
        "RATIONAL"     : (3, 6),   # (min, max) agents to follow
        "EMOTIONAL"    : (8, 15),  # highly connected — amplifies trends
        "TRIBAL"       : (5, 10),  # clustered by group
        "CONTRARIAN"   : (4, 8),   # diverse follows
        "INSTITUTIONAL": (2, 5)    # selective, formal network
    }

    def __init__(self):
        self.followers    = {}   # agent_id → list of agent_ids they follow
        self.round_posts  = {}   # agent_id → list of posts this round
        self.agents_by_type = {} # agent_type → list of agent objects
        self._agents      = []

    def build(self, agents: list):
        """
        Build the follower graph for all agents.
        Called once at the start of each simulation run.

        Follow logic:
        - Emotional agents follow the most people (amplifiers)
        - Tribal agents primarily follow same-type agents (echo chambers)
        - Contrarian agents deliberately follow some of everyone (diverse input)
        - Rational/Institutional agents follow selectively
        """
        self._agents = agents

        # Group agents by type for tribal clustering
        self.agents_by_type = {}
        for agent in agents:
            atype = getattr(agent, "agent_type", "UNKNOWN")
            if atype not in self.agents_by_type:
                self.agents_by_type[atype] = []
            self.agents_by_type[atype].append(agent)

        # Initialize empty follower lists
        for agent in agents:
            self.followers[agent.agent_id] = []
            self.round_posts[agent.agent_id] = []

        # Build follow relationships
        for agent in agents:
            atype = getattr(agent, "agent_type", "UNKNOWN")
            follow_range = self.FOLLOW_COUNTS.get(atype, (3, 6))
            n_follows = random.randint(*follow_range)

            # Cap at total available agents minus self
            other_agents = [a for a in agents if a.agent_id != agent.agent_id]
            n_follows = min(n_follows, len(other_agents))

            if n_follows == 0:
                continue

            if atype == "TRIBAL":
                # Tribal: 70% follows own type, 30% follows anyone
                same_type = [a for a in other_agents
                            if getattr(a, "agent_type", "") == atype]
                diff_type = [a for a in other_agents
                            if getattr(a, "agent_type", "") != atype]

                n_same = int(n_follows * 0.7)
                n_diff = n_follows - n_same

                follows = []
                if same_type:
                    follows += random.sample(same_type, min(n_same, len(same_type)))
                if diff_type:
                    follows += random.sample(diff_type, min(n_diff, len(diff_type)))

            elif atype == "CONTRARIAN":
                # Contrarian: deliberately diverse — follows at least one of each type
                follows = []
                for type_group in self.agents_by_type.values():
                    candidates = [a for a in type_group if a.agent_id != agent.agent_id]
                    if candidates:
                        follows.append(random.choice(candidates))
                # Fill remaining slots randomly
                remaining = n_follows - len(follows)
                if remaining > 0:
                    pool = [a for a in other_agents if a not in follows]
                    if pool:
                        follows += random.sample(pool, min(remaining, len(pool)))

            else:
                # Rational, Emotional, Institutional: random follows
                follows = random.sample(other_agents, n_follows)

            self.followers[agent.agent_id] = [a.agent_id for a in follows]

        # Print network summary
        total_connections = sum(len(v) for v in self.followers.values())
        print(f"  Social network built: {len(agents)} agents, "
              f"{total_connections} connections")
        for atype, group in self.agents_by_type.items():
            avg_follows = sum(
                len(self.followers.get(a.agent_id, []))
                for a in group
            ) / len(group) if group else 0
            print(f"    {atype:15}: {len(group)} agents, "
                  f"avg {avg_follows:.1f} follows each")

    def post(self, agent_id: str, agent_name: str, agent_type: str, content: str):
        """
        An agent publishes a post this round.
        Posts are cleared at the end of each round via clear_round_posts().
        """
        if not content:
            return
        # Format: "Name (TYPE): content"
        formatted = f"{agent_name} ({agent_type}): {content[:150]}"
        if agent_id not in self.round_posts:
            self.round_posts[agent_id] = []
        self.round_posts[agent_id].append(formatted)

    def get_feed(self, agent_id: str, max_posts: int = 4) -> str:
        """
        Return formatted social feed for this agent — posts from agents they follow.
        Called before each agent's think() so they can read what others posted.

        Returns empty string if agent follows nobody or nobody has posted yet.
        Returns formatted string: "What people you follow are saying:\n..."
        """
        follows = self.followers.get(agent_id, [])
        if not follows:
            return ""

        feed_posts = []
        for followed_id in follows:
            posts = self.round_posts.get(followed_id, [])
            feed_posts.extend(posts)

        if not feed_posts:
            return ""

        # Limit total feed size to avoid overloading prompts
        feed_posts = feed_posts[:max_posts]
        feed_text = "\n".join(f"  • {post}" for post in feed_posts)
        return f"What people you follow are saying:\n{feed_text}"

    def clear_round_posts(self):
        """Clear all posts from the current round. Called after every agent acts."""
        for agent_id in self.round_posts:
            self.round_posts[agent_id] = []

    def get_network_stats(self) -> dict:
        """Return statistics about the network for logging."""
        return {
            "total_agents"     : len(self._agents),
            "total_connections": sum(len(v) for v in self.followers.values()),
            "agents_by_type"   : {t: len(g) for t, g in self.agents_by_type.items()}
        }