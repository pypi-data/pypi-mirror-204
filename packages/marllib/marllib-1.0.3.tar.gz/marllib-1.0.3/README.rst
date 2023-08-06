

.. raw:: html

   <div align="center">
   <img src=docs/source/images/logo1.png width=65% />
   </div>



.. raw:: html

   <h1 align="center"> MARLlib: The Multi-agent Reinforcement Learning Library </h1>



.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: 
   :alt: GitHub license


.. image:: https://github.com/Replicable-MARL/MARLlib/workflows/test/badge.svg
   :target: https://github.com/Replicable-MARL/MARLlib/workflows/test/badge.svg
   :alt: test


.. image:: https://readthedocs.org/projects/marllib/badge/?version=latest
   :target: https://marllib.readthedocs.io/en/latest/
   :alt: Documentation Status


.. image:: https://img.shields.io/github/issues/Replicable-MARL/MARLlib
   :target: https://github.com/Replicable-MARL/MARLlib/issues
   :alt: GitHub issues
 

.. image:: https://img.shields.io/github/stars/Replicable-MARL/MARLlib
   :target: https://github.com/Replicable-MARL/MARLlib/stargazers
   :alt: GitHub stars
 

.. image:: https://img.shields.io/github/forks/Replicable-MARL/MARLlib
   :target: https://github.com/Replicable-MARL/MARLlib/network
   :alt: GitHub forks


.. image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/Replicable-MARL/MARLlib/blob/sy_dev/marllib.ipynb
   :alt: Open In Colab


**Multi-agent Reinforcement Learning Library (MARLlib)** is **\ *a comprehensive MARL algorithm library*\ ** based
on `\ **Ray** <https://github.com/ray-project/ray>`_ and one of its toolkits `\ **RLlib** <https://github.com/ray-project/ray/tree/master/rllib>`_. It provides MARL research community with a unified
platform for building, training, and evaluating MARL algorithms on almosty all kinds of diverse tasks and environments.

A simple case of MARLlib usage:

.. code-block:: py

   from marllib import marl

   # prepare env
   env = marl.make_env(environment_name="mpe", map_name="simple_spread")

   # initialize algorithm with appointed hyper-parameters
   mappo = marl.algos.mappo(hyperparam_source='mpe')

   # build agent model based on env + algorithms + user preference
   model = marl.build_model(env, mappo, {"core_arch": "gru", "encode_layer": "128-256"})

   # start training
   mappo.fit(env, model, stop={'timesteps_total': 1000000}, share_policy='group')

   # ready to control
   mappo.render(env, model, share_policy='group', restore_path='path_to_checkpoint')

Why MARLlib?
------------

Here we provide a table for the comparison of MARLlib and existing work.

.. list-table::
   :header-rows: 1

   * - Library
     - Github Stars
     - Supported Env
     - Algorithm
     - Parameter Sharing
     - Model
     - Framework
   * - `PyMARL <https://github.com/oxwhirl/pymarl>`_
     - 
     .. image:: https://img.shields.io/github/stars/oxwhirl/pymarl
        :target: https://github.com/oxwhirl/pymarl/stargazers
        :alt: GitHub stars
     
     - 1 cooperative
     - 5
     - share
     - GRU
     - *
   * - `MARL-Algorithms <https://github.com/starry-sky6688/MARL-Algorithms>`_
     - 
     .. image:: https://img.shields.io/github/stars/starry-sky6688/MARL-Algorithms
        :target: https://github.com/starry-sky6688/MARL-Algorithms/stargazers
        :alt: GitHub stars
     
     - 1 cooperative
     - 9
     - share
     - RNN
     - *
   * - `MAPPO Benchmark <https://github.com/marlbenchmark/on-policy>`_
     - 
     .. image:: https://img.shields.io/github/stars/marlbenchmark/on-policy
        :target: https://github.com/marlbenchmark/on-policy/stargazers
        :alt: GitHub stars
     
     - 4 cooperative
     - 1
     - share + separate
     - MLP / GRU
     - pytorch-a2c-ppo-acktr-gail
   * - `MAlib <https://github.com/sjtu-marl/malib>`_
     - 
     .. image:: https://img.shields.io/github/stars/sjtu-marl/malib
        :target: https://github.com/hijkzzz/sjtu-marl/malib/stargazers
        :alt: GitHub stars
     
     - 4 self-play
     - 10
     - share + group + separate
     - MLP / LSTM
     - *
   * - `EPyMARL <https://github.com/uoe-agents/epymarl>`_
     - 
     .. image:: https://img.shields.io/github/stars/uoe-agents/epymarl
        :target: https://github.com/hijkzzz/uoe-agents/epymarl/stargazers
        :alt: GitHub stars
     
     - 4 cooperative
     - 9
     - share + separate
     - GRU
     - PyMARL
   * - `MARLlib <https://github.com/Replicable-MARL/MARLlib>`_
     - 
     .. image:: https://img.shields.io/github/stars/Replicable-MARL/MARLlib
        :target: https://github.com/Replicable-MARL/MARLlib/stargazers
        :alt: GitHub stars
     
     - any task with **no task mode restriction**
     - 18
     - share + group + separate + customizable
     - MLP / CNN / GRU / LSTM
     - Ray/RLlib


What **MARLlib** brings to MARL community:


* MARLlib unifies diverse algorithm pipeline with agent-level distributed dataflow.
* MARLlib supports all task modes: cooperative, collaborative, competitive, and mixed.
* MARLlib unifies multi-agent environment interfaces with a new interface following Gym standard.
* MARLlib provides flexible and customizable parameter sharing strategies.

With MARLlib, you can exploit the advantages not limited to:


* out of the box **18 algorithms** including common baselines and recent state of the arts!
* **all task modes** available! cooperative, collaborative, competitive, and mixed (team-based
  competition)
* easy to incorporate new multi-agent environment!
* **customizable model arch**\ ! or pick your favorite one from MARLlib
* **customizable policy sharing** among agents! or grouped by MARLlib automatically
* more than a thousand experiments are conducted and released!

Installation
------------


* install dependencies
* install environments
* install patches

Install dependencies (basic)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First install MARLlib dependencies to guarantee basic usage.
following `this guide <https://marllib.readthedocs.io/en/latest/handbook/env.html>`_\ , finally install patches for RLlib.
After installation, training can be launched by following the usage section below.

.. code-block:: bash

   conda create -n marllib python=3.8
   conda activate marllib
   git clone https://github.com/Replicable-MARL/MARLlib.git
   cd MARLlib
   pip install --upgrade pip
   pip install -r requirements.txt

Note: **MPE** is included in basic installation.

Install environments (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please follow `this guide <https://marllib.readthedocs.io/en/latest/handbook/env.html>`_.

Install patches (basic)
^^^^^^^^^^^^^^^^^^^^^^^

Fix bugs of RLlib using patches by run the following command:

.. code-block:: bash

   cd /Path/To/MARLlib/marl/patch
   python add_patch.py -y

Learning with MARLlib
---------------------

There are four parts of configurations that take charge of the whole training process.


* scenario: specify the environment/task settings
* algorithm: choose the hyperparameters of the algorithm 
* model: customize the model architecture
* ray/rllib: change the basic training settings


.. raw:: html

   <div align="center">
   <img src=docs/source/images/configurations.png width=100% />
   </div>


*Note: You can modify all the pre-set parameters via MARLLib api.*

Pre-training
^^^^^^^^^^^^

Making sure all the dependency are installed for the environment you are running with.
Otherwise, please refer to the `doc <https://marllib.readthedocs.io/en/latest/handbook/env.html>`_. 

..

    **Note: Always check your ``gym`` version and keep it to ``0.21.0``.**


All environments MARLlib supported should work fine with this version.

MARLlib API
^^^^^^^^^^^

.. code-block:: py

   from marllib import marl
   # prepare env
   env = marl.make_env(environment_name="mpe", map_name="simple_spread")
   # initialize algorithm with appointed hyper-parameters
   mappo = marl.algos.mappo(hyperparam_source="mpe")
   # build agent model based on env + algorithms + user preference
   model = marl.build_model(env, mappo, {"core_arch": "mlp", "encode_layer": "128-256"})
   # start training
   mappo.fit(env, model, stop={"timesteps_total": 1000000}, checkpoint_freq=100, share_policy="group")

prepare the ``environment``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - task mode
     - api example
   * - cooperative
     - ``marl.make_env(environment_name="mpe", map_name="simple_spread", force_coop=True)``
   * - collaborative
     - ``marl.make_env(environment_name="mpe", map_name="simple_spread")``
   * - competitive
     - ``marl.make_env(environment_name="mpe", map_name="simple_adversary")``
   * - mixed
     - ``marl.make_env(environment_name="mpe", map_name="simple_crypto")``


Most of the popular environments in MARL research are supported by MARLlib:

.. list-table::
   :header-rows: 1

   * - Env Name
     - Learning Mode
     - Observability
     - Action Space
     - Observations
   * - **\ `LBF <https://github.com/semitable/lb-foraging>`_\ **
     - cooperative + collaborative
     - Both
     - Discrete
     - 1D
   * - **\ `RWARE <https://github.com/semitable/robotic-warehouse>`_\ **
     - cooperative
     - Partial
     - Discrete
     - 1D
   * - **\ `MPE <https://github.com/openai/multiagent-particle-envs>`_\ **
     - cooperative + collaborative + mixed
     - Both
     - Both
     - 1D
   * - **\ `SMAC <https://github.com/oxwhirl/smac>`_\ **
     - cooperative
     - Partial
     - Discrete
     - 1D
   * - **\ `MetaDrive <https://github.com/decisionforce/metadrive>`_\ **
     - collaborative
     - Partial
     - Continuous
     - 1D
   * - **\ `MAgent <https://www.pettingzoo.ml/magent>`_\ **
     - collaborative + mixed
     - Partial
     - Discrete
     - 2D
   * - **\ `Pommerman <https://github.com/MultiAgentLearning/playground>`_\ **
     - collaborative + competitive + mixed
     - Both
     - Discrete
     - 2D
   * - **\ `MAMuJoCo <https://github.com/schroederdewitt/multiagent_mujoco>`_\ **
     - cooperative
     - Partial
     - Continuous
     - 1D
   * - **\ `GRF <https://github.com/google-research/football>`_\ **
     - collaborative + mixed
     - Full
     - Discrete
     - 2D
   * - **\ `Hanabi <https://github.com/deepmind/hanabi-learning-environment>`_\ **
     - cooperative
     - Partial
     - Discrete
     - 1D


Each environment has a readme file, standing as the instruction for this task, including env settings, installation,
and important notes.

initialize the  ``algorithm``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - running target
     - api example
   * - train & finetune
     - ``marl.algos.mappo(hyperparam_source=$ENV)``
   * - develop & debug
     - ``marl.algos.mappo(hyperparam_source="test")``
   * - 3rd party env
     - ``marl.algos.mappo(hyperparam_source="common")``


Here is a chart describing the characteristics of each algorithm:

.. list-table::
   :header-rows: 1

   * - algorithm
     - support task mode
     - discrete action
     - continuous action
     - policy type
   * - *IQL**
     - all four
     - :heavy_check_mark:
     - 
     - off-policy
   * - *\ `PG <https://papers.nips.cc/paper/1713-policy-gradient-methods-for-reinforcement-learning-with-function-approximation.pdf>`_\ *
     - all four
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *\ `A2C <https://arxiv.org/abs/1602.01783>`_\ *
     - all four
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *\ `DDPG <https://arxiv.org/abs/1509.02971>`_\ *
     - all four
     - 
     - :heavy_check_mark:
     - off-policy
   * - *\ `TRPO <http://proceedings.mlr.press/v37/schulman15.pdf>`_\ *
     - all four
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *\ `PPO <https://arxiv.org/abs/1707.06347>`_\ *
     - all four
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *\ `COMA <https://ojs.aaai.org/index.php/AAAI/article/download/11794/11653>`_\ *
     - all four
     - :heavy_check_mark:
     - 
     - on-policy
   * - *\ `MADDPG <https://arxiv.org/abs/1706.02275>`_\ *
     - all four
     - 
     - :heavy_check_mark:
     - off-policy
   * - *MAA2C**
     - all four
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *MATRPO**
     - all four
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *\ `MAPPO <https://arxiv.org/abs/2103.01955>`_\ *
     - all four
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *\ `HATRPO <https://arxiv.org/abs/2109.11251>`_\ *
     - cooperative
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *\ `HAPPO <https://arxiv.org/abs/2109.11251>`_\ *
     - cooperative
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *\ `VDN <https://arxiv.org/abs/1706.05296>`_\ *
     - cooperative
     - :heavy_check_mark:
     - 
     - off-policy
   * - *\ `QMIX <https://arxiv.org/abs/1803.11485>`_\ *
     - cooperative
     - :heavy_check_mark:
     - 
     - off-policy
   * - *\ `FACMAC <https://arxiv.org/abs/2003.06709>`_\ *
     - cooperative
     - 
     - :heavy_check_mark:
     - off-policy
   * - *\ `VDAC <https://arxiv.org/abs/2007.12306>`_\ *
     - cooperative
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy
   * - *VDPPO**
     - cooperative
     - :heavy_check_mark:
     - :heavy_check_mark:
     - on-policy


***all four**\ : cooperative collaborative competitive mixed

*IQL* is the multi-agent version of Q learning.
*MAA2C* and *MATRPO* are the centralized version of A2C and TRPO.
*VDPPO* is the value decomposition version of PPO.

construct the agent  ``model``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - model arch
     - api example
   * - MLP
     - ``marl.build_model(env, algo, {"core_arch": "mlp")``
   * - GRU
     - ``marl.build_model(env, algo, {"core_arch": "gru"})``
   * - LSTM
     - ``marl.build_model(env, algo, {"core_arch": "lstm"})``
   * - encoder arch
     - ``marl.build_model(env, algo, {"core_arch": "gru", "encode_layer": "128-256"})``


kick off the training ``algo.fit``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - setting
     - api example
   * - train
     - ``algo.fit(env, model)``
   * - debug
     - ``algo.fit(env, model, local_mode=True)``
   * - stop condition
     - ``algo.fit(env, model, stop={'episode_reward_mean': 2000, 'timesteps_total': 10000000})``
   * - policy sharing
     - ``algo.fit(env, model, share_policy='all') # or 'group' / 'individual'``
   * - save model
     - ``algo.fit(env, model, checkpoint_freq=100, checkpoint_end=True)``
   * - GPU accelerate
     - ``algo.fit(env, model, local_mode=False, num_gpus=1)``
   * - CPU accelerate
     - ``algo.fit(env, model, local_mode=False, num_workers=5)``


policy inference ``algo.render``

.. list-table::
   :header-rows: 1

   * - setting
     - api example
   * - render
     - ``algo.render(env, model, local_mode=True, restore_path='path_to_model')``


By default, all the models will be saved at ``/home/username/ray_results/experiment_name/checkpoint_xxxx``

Tutorials
---------

Try MPE + MAPPO examples on Google Colaboratory!

.. image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/Replicable-MARL/MARLlib/blob/sy_dev/marllib.ipynb
   :alt: Open In Colab


Experiment Results
------------------

All results are listed `here <https://github.com/Replicable-MARL/MARLlib/tree/main/results>`_.
