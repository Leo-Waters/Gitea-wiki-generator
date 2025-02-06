namespace test
{
    enum state : byte
    {
        ON=1,
        OFF=0
    }

    interface IchargeAble 
    {
        void Charge();
        bool isCharged();
    }

    namespace sub
    {
        public class item
        {
            public virtual void Use()
            {
            
            }
        }

        public class sword : item , IchargeAble
        {
            void Attack()
            {
            
            }

            bool isCharged => true;

            public overide void Use => Attack();
        }
    
    }
}